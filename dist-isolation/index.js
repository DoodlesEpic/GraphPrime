window.__TAURI_ISOLATION_HOOK__ = (payload) => {
  // Guarantee that the hook is an object
  if (typeof payload !== "object") throw new Error("hook is not an object");

  // Guarantee that the hook command is one of the allowed commands
  if (!["calculate", "tauri", "__initialized"].includes(payload.cmd))
    throw new Error("Hook command is not one of the allowed commands");

  // If the cmd is "calculate" we should check for proper input
  if (payload.cmd === "calculate") {
    // Guarantee that the hook has a "callback", "x", "cmd", and "error" property
    if (
      !("callback" in payload) ||
      !("x" in payload.payload) ||
      !("cmd" in payload) ||
      !("error" in payload)
    ) {
      throw new Error("Hook does not have all properties");
    }

    // Gurantee that x, error, and callback are numbers, and that cmd is a string
    if (
      typeof payload.payload.x !== "number" ||
      typeof payload.error !== "number" ||
      typeof payload.callback !== "number" ||
      typeof payload.cmd !== "string"
    ) {
      throw new Error("Hook has invalid types");
    }

    // Guarantee that "x" is a positive number
    if (payload.payload.x <= 0) {
      console.error("x is not a positive number");
      throw new Error("Hook has invalid values");
    }
  }

  return payload;
};
