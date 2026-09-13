import http from "k6/http";

export const options = {
  stages: [
    {
      duration: "15s",
      target: 50,
    },
    {
      duration: "30s",
      target: 50,
    },
    {
      duration: "10s",
      target: 0,
    },
  ],
};

function randomString(length) {
  const chars = "abcdefghijklmnopqrstuvwxyz0123456789";
  let result = "";
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

export default function () {
  const rand = randomString(8);
  const payload = JSON.stringify({
    email: `user_${rand}@example.com`,
    fname: `Fname_${rand}`,
    lname: `Lname_${rand}`,
    password: "Pass" + randomString(6),
  });

  const headers = { "Content-Type": "application/json" };

  http.post("http://127.0.0.1:8001/auth/signup", payload, { headers });
}
