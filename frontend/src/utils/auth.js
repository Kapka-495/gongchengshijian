const TOKEN_KEY = 'token'
const USER_KEY = 'userInfo'

export function getToken() {
  return localStorage.getItem(TOKEN_KEY)
}

export function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token)
}

export function removeToken() {
  localStorage.removeItem(TOKEN_KEY)
}

export function getUserInfo() {
  const raw = localStorage.getItem(USER_KEY)
  return raw ? JSON.parse(raw) : null
}

export function setUserInfo(info) {
  localStorage.setItem(USER_KEY, JSON.stringify(info))
}

export function removeUserInfo() {
  localStorage.removeItem(USER_KEY)
}

export function clearAuth() {
  removeToken()
  removeUserInfo()
}
