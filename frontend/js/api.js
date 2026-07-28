/*
  api.js
  ------------------------------------------------------------
  Every page includes this file. It gives us one function,
  apiCall(), used to talk to the Flask backend under /api/...
  Because the frontend is served BY the same Flask app,
  we can use relative paths and the login cookie just works.
  ------------------------------------------------------------
*/

async function apiCall(path, method = "GET", body = null) {
    const options = {
        method,
        headers: { "Content-Type": "application/json" },
    };
    if (body) options.body = JSON.stringify(body);

    const response = await fetch(path, options);
    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
        throw new Error(data.error || "Something went wrong");
    }
    return data;
}
