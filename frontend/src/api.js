let onUnauthorized = () => {}
export function setUnauthorizedHandler(fn) { onUnauthorized = fn }

export async function api(path, options = {}) {
  const res = await fetch('/api' + path, { credentials: 'same-origin', ...options })
  if (res.status === 401) onUnauthorized()
  return res
} 