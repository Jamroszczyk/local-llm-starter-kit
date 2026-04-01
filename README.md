## Local LLM Showcase

This codebase demonstrates how to use **LM Studio** as a local LLM server and talk to it with simple Python scripts.

The two main entry points are:

- `local/local_llm_no_memory.py` – **single exchange**, no memory between runs.
- `local/local_llm_memory.py` – **ongoing chat**, with conversation state remembered via `previous_response_id` in LM Studio’s cache.

The `cloud/azure_llm.py` file is **not** part of the local setup; see the note at the end of this document before touching it.

---

## 1. Install LM Studio

1. Go to the official LM Studio download page and install it for your platform.
2. Launch LM Studio once installation is complete.

---

## 2. (Optional) Check Your Hardware in LM Studio

In LM Studio:

1. Open **Settings → Hardware**.
2. Review what your machine has:
   - **CPU only** (no dedicated GPU), and how much **system RAM** you have.
   - A **GPU**, its type, and how much **VRAM** it has.

This is optional but helps you reason about which models are realistic for your machine.

### GPU vs CPU, VRAM vs RAM – Rules of Thumb

- **With GPU**: Inference can be much faster; the limiting factor is usually **VRAM**.
- **Without GPU**: Inference runs on **CPU only** and uses **system RAM**. It can still work, but will be slower and more limited in model size.
- **Model size and parameters**:
  - Bigger models (more parameters, larger file size) generally need more **VRAM/RAM** and are slower.
  - Quantized models (smaller GB size for the same parameter count) are easier to run on limited hardware.

Very rough, conservative guide (assuming quantized models and default-ish LM Studio settings):

| Model (approx)              | Params | Typical quant file size | CPU only, 8 GB RAM | GPU 8 GB VRAM | GPU 16 GB VRAM |
|-----------------------------|--------|--------------------------|--------------------|---------------|----------------|
| Tiny (1–2B)                 | 1–2B   | 1–2 GB                   | **Probably**       | **Probably**  | **Probably**   |
| Small (3–4B)                | 3–4B   | 2–4 GB                   | **Borderline**     | **Probably**  | **Probably**   |
| Medium (7–8B)               | 7–8B   | 4–8 GB                   | **No**             | **Borderline**| **Probably**   |
| Large (12–14B)              | 12–14B | 8–14 GB                  | **No**             | **No**        | **Borderline** |
| Very large (30B+)           | 30B+   | 15 GB+                   | **No**             | **No**        | **No**         |

- **No**: Very unlikely to be usable on this setup.
- **Borderline**: Might load with careful settings and smaller context windows, but expect slowness and possible out‑of‑memory errors.
- **Probably**: Reasonable chance of working at usable speeds.

These are just guidelines. Exact behavior depends on your hardware, the specific quant, LM Studio’s context window settings, and many other low‑level details.

If you are unsure, **stick to smaller models around 1–3B parameters**, download quants of **~1–3 GB**, and keep LM Studio settings at their defaults. LM Studio’s UI also tries to signal which models are likely to work on your machine—hover the icons in the model search to see what they mean.

---

## 3. Enable Developer Mode in LM Studio

In LM Studio:

1. Open **Settings → Developer**.
2. Enable **Developer Mode**.
3. Close the settings.

---

## 4. Download Your First Model

1. In LM Studio, use the **Model search**.
2. Download a small instruction model.  
   - **Recommendation**: `llama-3.2-3b-instruct` (or similar “3B instruct” model).  
     - It’s fast to download.
     - It runs on very limited hardware (laptops, some smartphones, etc.).

Once the model has finished downloading, proceed to the next step.

---

## 5. Start the Local Server and Load the Model

1. In LM Studio, open the **Developer** tab in the right sidebar (not in Settings).
2. In the **Server** card:
   - Turn on the toggle next to **Status** if it is not already on.  
   - It should show the status **“running”**.
3. In the same card, click **“Load Model”** and select the model you just downloaded.
4. After loading, the model should appear under **Loaded Models** in this view.

On this page, note two important pieces of information that we will use in our code:

- **Endpoint** shown as **“reachable at”** – by default this is `http://127.0.0.1:1234`.
- **Model name** in the loaded model card – e.g. `llama-3.2-3b-instruct`.

---

## 6. Configure the Python Scripts

In this repository, you can talk to the local LM Studio server using:

- `local/local_llm_no_memory.py`
- `local/local_llm_memory.py`

In both scripts, locate and update the variables:

- `endpoint`
- `model`

Use the values from the LM Studio **Developer** page:

- From the **“reachable at”** field, e.g. `http://127.0.0.1:1234`.
- From the **loaded model name**, e.g. `llama-3.2-3b-instruct`.

To use the **chat endpoint**, you must append `/api/v1/chat` to the base URL:

- If LM Studio shows `http://127.0.0.1:1234` as the endpoint, then in the code set:
  - `endpoint = "http://127.0.0.1:1234/api/v1/chat"`

For example:

```python
endpoint = "http://127.0.0.1:1234/api/v1/chat"
model = "llama-3.2-3b-instruct"
```

That’s it. Once those values are set correctly, you can execute the scripts and communicate with the loaded model from your terminal.

---

## 7. How the Scripts Work

### `local_llm_no_memory.py` – Single Exchange

- This script performs **one request–response exchange** with the model.
- There is **no memory** between runs: every time you execute the script, it starts “fresh”.
- You can control whether you see only the generated text or the **full response payload** from LM Studio:
  - The `chat` function has a `full_data` parameter.
  - If you set `full_data=True` when calling it, you’ll see the entire JSON data that LM Studio returns.

### `local_llm_memory.py` – Ongoing Chat with Memory

- This script contains the chat logic inside a **recursive function**.
- In addition to the standard payload, it also sends a `previous_response_id` to LM Studio.
- LM Studio uses `previous_response_id` to access previously sent messages from its internal cache, so you do **not** need to resend the entire chat history (unlike many cloud APIs).
- When you run `local_llm_memory.py`, it starts an **infinite loop** where you can have a back‑and‑forth conversation with the model, and it will remember previous context.
  - Type `exit` to break out of the loop and end the script.

You can freely switch models in LM Studio, play with hyperparameters, and experiment with prompt engineering. The exact capabilities and options depend strongly on the model you are using and the payload shape that model expects or returns.

---

## 8. Practical Limits and Things to Watch

Your local machine **cannot** handle an infinitely large model, infinitely long prompts, or infinitely long conversations. The real limits depend on:

- **Your hardware** (CPU speed, number of cores, RAM size, GPU VRAM, etc.).
- **Model complexity** (number of parameters).
- **Model file size** (in GB, often correlated with parameter count and quantization).
- **Model’s maximum context window**.
- **LM Studio server settings** (especially maximum context length and memory allocation).

LM Studio offers many settings to handle overflow and limit inference. If you are unsure:

- Prefer **smaller models** in the **1–3B parameter** range.
- Download **quantized model snapshots** with file sizes around **1–3 GB**.
- Leave LM Studio’s server settings at their **defaults**.
- Use LM Studio’s UI hints: it will show icons indicating whether a given quant is likely to work on your hardware. Hover those icons to see details.

As you become more comfortable, it’s worth doing a deeper dive into how model size, quantization level, context window, and hardware interact.

---

## 9. Cloud / Azure Note

This repo also contains:

- `cloud/azure_llm.py`

This script is **not** meant for casual use and **should not be modified or run unless you know what you are doing**. It:

- Requires a **paid Azure subscription**.
- Depends on deploying resources and models in **Microsoft Azure AI / Model Catalog (Foundry)**.
- Is tied to **real cloud costs** when used.

You can safely **ignore** this file for local experiments. It is included for **future showcases** and advanced cloud integration examples.

---

## 10. Summary

- Use LM Studio as a **local LLM server**.
- Configure `endpoint` (with `/api/v1/chat` appended) and `model` in the Python scripts to match LM Studio’s **Developer** view.
- Use `local_llm_no_memory.py` for **one‑shot** calls.
- Use `local_llm_memory.py` for **multi‑turn chat with memory** via `previous_response_id`.

