# Hallucination & Fact-Drift Detection Report

## Summary
- **Total prompts analyzed**: 5
- **Hallucinations detected**: 4
- **Hallucination rate**: 80.0%
- **Average similarity**: 0.112
- **Overall quality**: Poor

## Individual Analysis

### Prompt 1: What is the capital of France?
**Generated**: france

**Reference**: Paris is the capital of France.

**Similarity Score**: 0.000

**Status**: 🚨 POTENTIAL HALLUCINATION

---

### Prompt 2: Who invented the computer?
**Generated**: george w. bush

**Reference**: Charles Babbage is often credited with inventing the first mechanical computer.

**Similarity Score**: 0.000

**Status**: 🚨 POTENTIAL HALLUCINATION

---

### Prompt 3: When did the Berlin Wall fall?
**Generated**: 1927

**Reference**: The Berlin Wall fell on November 9, 1989.

**Similarity Score**: 0.000

**Status**: 🚨 POTENTIAL HALLUCINATION

---

### Prompt 4: What is 5 + 7?
**Generated**: 5 + 7

**Reference**: 5 + 7 equals 12.

**Similarity Score**: 0.559

**Status**: ✅ FACTUAL

---

### Prompt 5: Who wrote Harry Potter?
**Generated**: edward w. kennedy

**Reference**: J.K. Rowling wrote the Harry Potter series.

**Similarity Score**: 0.000

**Status**: 🚨 POTENTIAL HALLUCINATION

---

## Consistency Analysis
- **Average consistency**: 0.026
- **Minimum consistency**: 0.000
- **Is inconsistent**: True

