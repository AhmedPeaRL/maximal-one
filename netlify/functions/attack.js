export async function handler(event) {
  try {
    const body = JSON.parse(event.body || "{}");

    if (!body.attack) {
      return { statusCode: 400, body: "No attack provided" };
    }

    // مجرد تسجيل للهجوم
    console.log("External attack:", body.attack);

    return {
      statusCode: 200,
      body: JSON.stringify({
        accepted: true,
        message: "Attack recorded and will be evaluated"
      })
    };

  } catch (e) {
    return { statusCode: 500, body: "Error" };
  }
}
