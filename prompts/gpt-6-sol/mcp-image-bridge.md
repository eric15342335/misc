---
name: mcp-image-bridge
description: Use when an MCP tool returns image bytes as Base64 text or a nested image block inside ChatGPT functions.exec, but the model cannot see the image. Forward that one image through image() in the same execution; not for image search or generation.
---

# MCP Image Bridge

Call the MCP tool and `image()` **inside the same `functions.exec` call**. Inspect the actual response schema. Never print Base64 into text output. If the result contains an MCP `ImageContent` block, use `image(block, "original")` directly.

For Base64, extract the real response field, join any chunks in order, and use the correct MIME type:

```javascript
const r = await tools[toolName](args);  // toolName/args from MCP tool discovery
const raw = r.result.content;          // replace with actual Base64 field or joined chunks
const mime = "image/webp";             // replace with the image's actual MIME type
if (typeof raw !== "string" || !raw.trim()) throw Error("Missing image data");
image(`data:${mime};base64,${raw.replace(/\s/g, "")}`, "original");
```

`image()` is a `functions.exec` output helper, not a standard MCP API. If it fails, report the failure; do not claim to have seen the image.
