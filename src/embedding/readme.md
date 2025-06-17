## 🧩 PEFT (Parameter-Efficient Fine-Tuning) Workflow

This project supports parameter-efficient fine-tuning (PEFT) using Hugging Face’s [peft](https://github.com/huggingface/peft) library.

### How it works

1. **Prepare data:**  
   Run the pipeline to generate cleaned code and documentation chunks in `data/clean/`.

2. **Configure PEFT:**  
   Edit `config.yaml` to set PEFT parameters (method, LoRA rank, epochs, batch size, etc.).
   - To enable supervised fine-tuning, set `supervised: true` under `peft:` and ensure data entries include a `label` field.

3. **Run fine-tuning:**  
   ```sh
   python src/embedding/peft_finetune.py
   ```
   This will use actual cleaned data for fine-tuning.

4. **Use the adapter:**  
   The resulting PEFT adapter is saved to the directory specified in config.  
   The embedder will automatically load this adapter for inference if present.

---

**Sage Wisdom:**  
_“Document  workflow and support both supervised and unsupervised learning for maximum flexibility.”_