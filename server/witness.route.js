const express = require("express");
const router = express.Router();

const { allowOnce } = require("../gate/conditional.gate");
const { process } = require("../processor/process_once");
const { emit } = require("../artifacts/emit");

router.post("/record", (req, res) => {
  if (!allowOnce()) return res.status(204).end();

  const artifact = process(req.body);
  emit(artifact);
  res.status(204).end();
});

module.exports = router;
