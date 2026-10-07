#!/usr/bin/env bash
# Fail if an AppImage contains a file or directory with owner-only permissions.
set -euo pipefail

image="${1:?usage: $0 <file.AppImage>}"

command -v unsquashfs >/dev/null
[ -x "$image" ] || chmod +x "$image"
offset="$("$(realpath "$image")" --appimage-offset)"
[[ "$offset" =~ ^[0-9]+$ ]] && (( offset > 0 ))

listing="$(unsquashfs -lln -o "$offset" "$image")"

bad="$(awk '
  $1 ~ /^[-d]/ {
    m = $1
    owner_x = substr(m, 4, 1) ~ /[xs]/
    other_r = substr(m, 8, 1) == "r"
    other_x = substr(m, 10, 1) ~ /[xt]/
    if ((owner_x && !other_x) || !other_r) {
      path = $0; sub(/^.*squashfs-root\/?/, "", path)
      print m, path
    }
  }' <<<"$listing")"

if [ -n "$bad" ]; then
  echo "::error::AppImage contains owner-only permissions; non-root users cannot run it:"
  echo "$bad"
  exit 1
fi

echo "AppImage modes verified: all entries in $(basename "$image") are accessible by any user."
