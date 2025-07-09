import http from "k6/http";

export const options = {
  stages: [
    {
      duration: "15s",
      target: 20,
    },
    {
      duration: "30s",
      target: 20,
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

const TOKEN =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtaWFkYWJkaUBnbWFpbC5jb20iLCJleHAiOjE3NTIxMDYzNzd9.05iCCLDbVhvZ03LfPwhZzDrHZv-8Mm1_ydUdBFyIxqE";

export default function () {
  const rand = randomString(8);

  const payload = JSON.stringify({
    title: `Title ${rand}`,
    summary: `Summary ${rand}`,
    body: `Body content for ${rand}`,
    featured_image: `https://example.com/images/${rand}.jpg`,
    category_ids: [1], // You can randomize IDs if needed
    tag_ids: [1],
  });

  const headers = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${TOKEN}`,
  };
  http.post("http://127.0.0.1:8081/post/", payload, { headers });
}
