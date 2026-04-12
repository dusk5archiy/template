# =============================================================================

get-os() {
  . /etc/os-release
  echo "$ID"
}

# =============================================================================

sync-packages() {
  case "$(get-os)" in
  arch | msys2)
    pacman -Syu --noconfirm
    ;;
  ubuntu)
    apt update
    apt upgrade -y
    ;;
  esac
}

# =============================================================================

install-packages() {
  if [[ ${#packages[@]} -eq 0 ]]; then
    return
  fi

  sync-packages

  case "$(get-os)" in
  arch | msys2)
    pacman -S -noconfirm --needed "${packages[@]}"
    ;;
  ubuntu)
    apt install -y --no-install-recommends "${packages[@]}"
    ;;
  esac
}

# =============================================================================

install-python() {
  case "$(get-os)" in
  arch | msys2)
    install-packages python
    ;;
  ubuntu)
    install-packages python_is_python3 python3 python3-venv
    ;;
  esac
}

# =============================================================================
