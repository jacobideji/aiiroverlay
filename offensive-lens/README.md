# Step 10 (B1): Add the lens documents

One lens per Minimum Viable Overlay control. Each technique has a premise, a numbered procedure, PASS/PARTIAL/FAIL criteria and the defensive signal that should have fired.

## Run

From the root of your `aiiroverlay` clone. `$D` points at the folder these steps live in, which stays **outside** the clone: the clone gets its own `offensive-lens/` directory in step 10, and that is the component rather than these instructions.

```bash
D=/path/to/IR-Overlay-Offensive-Lens/offensive-lens
"$D/10-B1-documents/apply.sh"
"$D/10-B1-documents/verify.sh"
```

## Commit

```bash
git commit -F "$D/10-B1-documents/commit-message.txt"
```
