import fs from "fs";
import path from "path";

const filePath = path.join(process.cwd(), "config.json");

export default function handler(req, res) {
  if (req.method === "GET") {
    const file = fs.readFileSync(filePath, "utf-8");
    const config = JSON.parse(file);
    return res.status(200).json(config);
  }

  if (req.method === "POST") {
    const current = JSON.parse(fs.readFileSync(filePath, "utf-8"));
    const updated = { ...current, ...req.body };
    fs.writeFileSync(filePath, JSON.stringify(updated, null, 2), "utf-8");
    return res.status(200).json({ success: true, config: updated });
  }

  res.setHeader("Allow", ["GET", "POST"]);
  res.status(405).end(`Method ${req.method} Not Allowed`);
}
