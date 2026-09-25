"use strict";

const identity = document.getElementById("identity");
const question = document.getElementById("question");
const form = document.getElementById("ask-form");
const button = document.getElementById("ask-button");
const messages = document.getElementById("messages");
const topicTree = document.getElementById("topic-tree");
const sourceDialog = document.getElementById("source-dialog");
const sourceTitle = document.getElementById("source-title");
const sourceMeta = document.getElementById("source-meta");
const sourceLines = document.getElementById("source-lines");
const welcome = document.getElementById("empty").cloneNode(true);
let viewGeneration = 0;
let topicRequest = 0;
let sourceRequest = 0;

const STATE_LABELS = {
  answered: "Supported answer",
  answered_with_warning: "Answer with source warning",
  insufficient_evidence: "Not enough supporting information",
  conflicting_evidence: "Sources need owner review",
  no_authorized_evidence: "No accessible information for this employee",
  identity_denied: "Employee not recognized",
  invalid_request: "Question needs attention",
};

function clearMessages() {
  viewGeneration += 1;
  sourceRequest += 1;
  if (sourceDialog.open) sourceDialog.close();
  messages.replaceChildren();
  messages.append(welcome.cloneNode(true));
}

function addMessage(label, text, kind) {
  document.getElementById("empty")?.remove();
  const card = document.createElement("div");
  card.className = `message message-${kind}`;
  const heading = document.createElement("div");
  heading.className = "message-label";
  heading.textContent = label;
  const content = document.createElement("div");
  content.textContent = text; // Never render document text as HTML or Markdown.
  card.append(heading, content);
  messages.append(card);
  messages.scrollTop = messages.scrollHeight;
  return content;
}

async function openSource(source, selectedUser, requestGeneration) {
  if (identity.value !== selectedUser || viewGeneration !== requestGeneration) return;
  const request = ++sourceRequest;
  sourceTitle.textContent = "Loading source…";
  sourceMeta.textContent = "";
  sourceLines.replaceChildren();
  sourceDialog.showModal();
  try {
    const url = `/api/source?user_id=${encodeURIComponent(selectedUser)}&citation_id=${encodeURIComponent(source.citation_id)}`;
    const response = await fetch(url, { cache: "no-store" });
    if (!response.ok) throw new Error("Source unavailable");
    const detail = await response.json();
    if (identity.value !== selectedUser || viewGeneration !== requestGeneration || request !== sourceRequest || !sourceDialog.open) return;
    sourceTitle.textContent = detail.title;
    sourceMeta.textContent = `${detail.document_id} · v${detail.version} · ${detail.status} · ${detail.source_path} · cited lines ${detail.line_start}–${detail.line_end}`;
    let citedLine = null;
    for (const line of detail.lines) {
      const row = document.createElement("div");
      row.className = "source-line";
      if (line.number >= detail.line_start && line.number <= detail.line_end) {
        row.classList.add("source-line-cited");
        if (line.number === detail.line_start) citedLine = row;
      }
      const number = document.createElement("span");
      number.className = "source-line-number";
      number.textContent = String(line.number);
      const text = document.createElement("span");
      text.textContent = line.text;
      row.append(number, text);
      sourceLines.append(row);
    }
    citedLine?.scrollIntoView({ block: "center" });
  } catch (_) {
    if (identity.value === selectedUser && viewGeneration === requestGeneration && request === sourceRequest && sourceDialog.open) {
      sourceTitle.textContent = "Source unavailable";
      sourceMeta.textContent = "This source is not available to the selected employee. It may be restricted, changed, or an invalid link.";
    }
  }
}

function sourceButton(source, label, selectedUser, requestGeneration) {
  const link = document.createElement("button");
  link.type = "button";
  link.className = "source-link";
  link.textContent = label;
  link.addEventListener("click", () => openSource(source, selectedUser, requestGeneration));
  return link;
}

function renderAnswer(target, result, selectedUser, requestGeneration) {
  target.replaceChildren();
  const state = document.createElement("div");
  state.className = "answer-state";
  state.textContent = STATE_LABELS[result.state] || "Response unavailable";
  if (!["answered", "answered_with_warning"].includes(result.state)) {
    state.classList.add("answer-state-caution");
  }
  target.append(state);

  if (!result.claims.length) {
    const message = document.createElement("p");
    message.className = "mb-0";
    message.textContent = result.answer;
    target.append(message);
    return;
  }

  if (result.notice) {
    const notice = document.createElement("p");
    notice.className = "alert alert-warning py-2 mb-3";
    notice.textContent = result.notice;
    target.append(notice);
  }

  const claims = document.createElement("ul");
  claims.className = "answer-claims mb-3";
  for (const claim of result.claims) {
    const item = document.createElement("li");
    item.append(document.createTextNode(`${claim.text} `));
    for (const id of claim.citations) {
      const index = result.sources.findIndex((source) => source.citation_id === id);
      if (index >= 0) {
        item.append(sourceButton(result.sources[index], `[${index + 1}]`, selectedUser, requestGeneration));
      }
    }
    claims.append(item);
  }
  target.append(claims);

  const heading = document.createElement("div");
  heading.className = "fw-semibold border-top pt-3 mb-2";
  heading.textContent = "Sources";
  target.append(heading);
  const sources = document.createElement("ol");
  sources.className = "source-list small mb-0";
  for (const source of result.sources) {
    const item = document.createElement("li");
    item.append(sourceButton(source, `${source.title} (${source.document_id}, v${source.version}, ${source.status}), lines ${source.line_start}–${source.line_end}`, selectedUser, requestGeneration));
    sources.append(item);
  }
  target.append(sources);
}

function renderTopicTree(areas) {
  topicTree.replaceChildren();
  if (!areas.length) {
    topicTree.textContent = "No available topics for this employee.";
    return;
  }
  for (const area of areas) {
    const group = document.createElement("section");
    group.className = "topic-area";
    const title = document.createElement("div");
    title.className = "topic-area-title";
    title.textContent = area.label;
    group.append(title);
    for (const topic of area.topics) {
      const item = document.createElement("div");
      const picker = document.createElement("button");
      picker.type = "button";
      picker.className = "topic-button";
      picker.title = topic.summary;
      const name = document.createElement("span");
      name.textContent = topic.label;
      const count = document.createElement("span");
      count.className = "topic-count";
      count.textContent = String(topic.sources.length);
      picker.append(name, count);
      picker.addEventListener("click", () => {
        question.value = topic.example_question;
        question.focus();
        if (window.innerWidth < 850) document.body.classList.add("sb-sidenav-toggled");
      });
      item.append(picker);
      const sources = document.createElement("ul");
      sources.className = "topic-sources";
      for (const source of topic.sources) {
        const line = document.createElement("li");
        line.textContent = `${source.title} · v${source.version} · ${source.status}`;
        sources.append(line);
      }
      item.append(sources);
      group.append(item);
    }
    topicTree.append(group);
  }
}

async function loadTopicTree() {
  const selectedUser = identity.value;
  const request = ++topicRequest;
  topicTree.textContent = "Loading available topics…";
  try {
    const response = await fetch(`/api/context?user_id=${encodeURIComponent(selectedUser)}`);
    if (!response.ok) throw new Error("Context unavailable");
    const result = await response.json();
    if (identity.value === selectedUser && request === topicRequest) {
      renderTopicTree(result.areas);
    }
  } catch (_) {
    if (identity.value === selectedUser && request === topicRequest) {
      topicTree.textContent = "Topic navigation is unavailable. You can still ask a question.";
    }
  }
}

identity.addEventListener("change", clearMessages);
identity.addEventListener("change", loadTopicTree);
document.getElementById("source-close").addEventListener("click", () => {
  sourceRequest += 1;
  sourceDialog.close();
});
document.getElementById("new-chat").addEventListener("click", () => {
  clearMessages();
  question.value = "";
  question.focus();
});
question.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    form.requestSubmit();
  }
});
loadTopicTree();

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const text = question.value.trim();
  if (!text || button.disabled) return;
  const selectedUser = identity.value;
  const requestGeneration = viewGeneration;
  addMessage(`Question · ${identity.selectedOptions[0].textContent}`, text, "user");
  const output = addMessage("Answer", "Checking authorized evidence…", "assistant");
  question.value = "";
  button.disabled = true;
  try {
    const response = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: selectedUser, question: text }),
    });
    if (!response.ok) throw new Error("Request failed");
    const result = await response.json();
    // A late response must not appear under a newly selected identity.
    if (identity.value === selectedUser && viewGeneration === requestGeneration) {
      renderAnswer(output, result, selectedUser, requestGeneration);
    }
  } catch (_) {
    if (identity.value === selectedUser && viewGeneration === requestGeneration) {
      output.textContent = "The local service could not answer. Please try again.";
    }
  } finally {
    button.disabled = false;
    question.focus();
  }
});
