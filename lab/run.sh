#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-jellyfin-suggestions-idor}"
export PYTHONUNBUFFERED=1
chmod +x poc.py

LABEL="jellyfin-suggestions-idor"
WITNESS="JELLYFIN-SUGGESTIONS-IDOR-WITNESS"
IMAGE_DEFAULT="jellyfin/jellyfin:12.2"
IMAGE_FALLBACKS=(
  "jellyfin/jellyfin:12.2"
  "jellyfin/jellyfin:12.2.20261005"
  "jellyfin/jellyfin:12.2.20261005-225228"
)

down() {
  echo "== docker compose down -v =="
  docker compose -p "${COMPOSE_PROJECT_NAME}" down -v --remove-orphans || true
}

fail_setup() {
  local reason="$1"
  echo "FAIL ${LABEL} ${reason} ${WITNESS}" | tee poc-last-run.txt
  docker compose -p "${COMPOSE_PROJECT_NAME}" logs --no-color --tail=80 jellyfin || true
  down
  exit 1
}

pick_image() {
  local img
  if [[ -n "${JELLYFIN_IMAGE:-}" ]]; then
    echo "== docker pull ${JELLYFIN_IMAGE} =="
    docker pull "${JELLYFIN_IMAGE}" || fail_setup "image-pull-failed"
    return
  fi
  for img in "${IMAGE_FALLBACKS[@]}"; do
    echo "== docker pull ${img} =="
    if docker pull "${img}"; then
      export JELLYFIN_IMAGE="${img}"
      return
    fi
    echo "IOC image-pull-miss ${img}"
  done
  fail_setup "image-pull-failed"
}

make_mp4() {
  local dest="$1"
  local dir
  dir="$(cd "$(dirname "${dest}")" && pwd)"
  local base
  base="$(basename "${dest}")"
  if command -v ffmpeg >/dev/null 2>&1; then
    ffmpeg -hide_banner -loglevel error -y \
      -f lavfi -i "color=c=black:s=64x64:d=1" \
      -c:v libx264 -pix_fmt yuv420p -t 1 "${dest}" \
      && return 0
    ffmpeg -hide_banner -loglevel error -y \
      -f lavfi -i "color=c=black:s=64x64:d=1" \
      -c:v mpeg4 -t 1 "${dest}" \
      && return 0
  fi
  local entry
  for entry in /usr/lib/jellyfin-ffmpeg/ffmpeg ffmpeg; do
    if docker run --rm --entrypoint "${entry}" \
      -v "${dir}:/out" \
      "${JELLYFIN_IMAGE:-${IMAGE_DEFAULT}}" \
      -hide_banner -loglevel error -y \
      -f lavfi -i "color=c=black:s=64x64:d=1" \
      -c:v libx264 -pix_fmt yuv420p -t 1 "/out/${base}"; then
      return 0
    fi
    if docker run --rm --entrypoint "${entry}" \
      -v "${dir}:/out" \
      "${JELLYFIN_IMAGE:-${IMAGE_DEFAULT}}" \
      -hide_banner -loglevel error -y \
      -f lavfi -i "color=c=black:s=64x64:d=1" \
      -c:v mpeg4 -t 1 "/out/${base}"; then
      return 0
    fi
  done
  return 1
}

trap down EXIT

echo "== docker compose down (clean) =="
down

pick_image
export JELLYFIN_IMAGE="${JELLYFIN_IMAGE:-${IMAGE_DEFAULT}}"
echo "IOC image=${JELLYFIN_IMAGE}"

echo "== seed media =="
rm -rf media
mkdir -p "media/private-a/${WITNESS}" "media/public-b/PublicBLab"
if ! make_mp4 "media/private-a/${WITNESS}/${WITNESS}.mp4"; then
  fail_setup "ffmpeg-private-failed"
fi
if ! make_mp4 "media/public-b/PublicBLab/PublicBLab.mp4"; then
  fail_setup "ffmpeg-public-failed"
fi
ls -la "media/private-a/${WITNESS}" "media/public-b/PublicBLab"

echo "== docker compose up =="
up_ok=0
for attempt in $(seq 1 8); do
  if JELLYFIN_IMAGE="${JELLYFIN_IMAGE}" docker compose -p "${COMPOSE_PROJECT_NAME}" up -d; then
    up_ok=1
    break
  fi
  echo "IOC compose-up-retry attempt=${attempt}"
  sleep 20
  down
done
if [[ "${up_ok}" != 1 ]]; then
  fail_setup "compose-up-failed"
fi

echo "== wait GET /Startup/User =="
ready=0
for i in $(seq 1 120); do
  code="$(curl -sS -o /tmp/jellyfin-suggestions-idor-startup-user.txt -w '%{http_code}' --max-time 8 \
    "http://127.0.0.1:18790/Startup/User" || true)"
  if [[ "${code}" == "200" ]] && grep -q '{' /tmp/jellyfin-suggestions-idor-startup-user.txt; then
    ready=1
    echo "IOC jellyfin-ready attempt=${i} startup-user=${code}"
    break
  fi
  echo "IOC jellyfin-wait attempt=${i} startup-user=${code}"
  sleep 3
done
if [[ "${ready}" != 1 ]]; then
  fail_setup "jellyfin-not-ready"
fi

echo "== poc.py =="
set +e
python3 ./poc.py | tee poc-last-run.txt
rc=${PIPESTATUS[0]}
set -e

if ! tail -n1 poc-last-run.txt 2>/dev/null | grep -qE '^(SUCCESS|FAIL) '; then
  echo "FAIL ${LABEL} poc-exit=${rc} ${WITNESS}" >> poc-last-run.txt
  rc=1
fi

exit "${rc}"
