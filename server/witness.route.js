const express = require("express");
const router = express.Router();

const { allowOnce } = require("../gate/conditional.gate");
const { process } = require("../processor/process_once");
const { emit } = require("../artifacts/emit");
const { sovereignGate } = require("../gate/sovereign.gate");
const { coldStore } = require("../store/cold.store");

router.post("/record", (req, res) => {
  if (!allowOnce()) return res.status(204).end();

  const artifact = process(req.body);
  emit(artifact);
  res.status(204).end();

if (!sovereignGate()) return res.status(204).end();
  coldStore(req.body);
  res.status(204).end();

router.post("/record", express.json(), (req, res) => {
  if (!allow()) return res.status(204).end();
  store(req.body);
  res.status(204).end();
});

module.exports = router;
