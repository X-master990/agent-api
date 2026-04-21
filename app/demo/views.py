from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("", response_class=HTMLResponse)
async def demo_page() -> str:
    return HTML


HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>TrustMesh Customer Demo</title>
  <style>
    :root {
      --ink:#17211f; --muted:#63706b; --paper:#fbf3e4; --pine:#173f36;
      --moss:#718f3f; --amber:#d98b29; --coral:#d75c47; --sky:#8fc4c7;
      --line:rgba(23,33,31,.14); --glass:rgba(255,252,244,.78);
      --shadow:0 30px 90px rgba(23,63,54,.22);
    }
    *{box-sizing:border-box}
    body{
      margin:0; min-height:100vh; color:var(--ink);
      font-family:"Avenir Next","Gill Sans","Trebuchet MS",sans-serif;
      background:
        radial-gradient(circle at 16% 12%,rgba(217,139,41,.26),transparent 31%),
        radial-gradient(circle at 86% 18%,rgba(143,196,199,.36),transparent 30%),
        linear-gradient(145deg,#fbf3e4 0%,#e9ead8 52%,#d6e1d1 100%);
    }
    body:before{
      content:""; position:fixed; inset:0; pointer-events:none;
      background-image:linear-gradient(rgba(23,33,31,.045) 1px,transparent 1px),
        linear-gradient(90deg,rgba(23,33,31,.045) 1px,transparent 1px);
      background-size:42px 42px; mask-image:linear-gradient(to bottom,#000,transparent 82%);
    }
    .shell{width:min(1180px,calc(100% - 32px)); margin:auto; padding:36px 0 54px}
    .hero{display:grid; grid-template-columns:1.08fr .92fr; gap:24px; animation:rise .7s ease both}
    .card,.panel,.step,.decision{background:var(--glass); border:1px solid rgba(255,255,255,.62); box-shadow:var(--shadow); backdrop-filter:blur(18px)}
    .card{border-radius:34px; padding:42px; overflow:hidden; position:relative}
    .card:after{content:""; position:absolute; width:270px; height:270px; right:-110px; top:-120px; border-radius:50%; background:rgba(113,143,63,.18)}
    .eyebrow{display:inline-flex; align-items:center; gap:10px; border:1px solid var(--line); border-radius:999px; padding:8px 12px; font-weight:900; font-size:12px; letter-spacing:.08em; text-transform:uppercase; color:var(--pine); background:rgba(255,255,255,.45)}
    .dot{width:9px;height:9px;border-radius:50%;background:var(--moss);box-shadow:0 0 0 6px rgba(113,143,63,.16)}
    h1{font-family:"Iowan Old Style","Palatino",Georgia,serif; font-size:clamp(44px,7vw,84px); line-height:.92; letter-spacing:-.065em; margin:26px 0 18px; max-width:760px}
    .lead{font-size:19px; line-height:1.65; color:#43514d; max-width:650px; margin:0}
    .metrics{display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-top:34px}
    .metric{border:1px solid var(--line); background:rgba(255,255,255,.45); border-radius:22px; padding:18px}
    .metric strong{font-family:"Iowan Old Style","Palatino",serif; font-size:27px; display:block}
    .metric span{color:var(--muted); font-size:13px; line-height:1.4}
    .control{border-radius:34px; padding:30px; display:flex; flex-direction:column; justify-content:space-between; min-height:420px}
    .scenario{border-radius:26px; padding:24px; color:#fff8e8; background:linear-gradient(135deg,rgba(23,63,54,.96),rgba(23,33,31,.93)); overflow:hidden; position:relative}
    .scenario:after{content:""; position:absolute; width:210px; height:210px; right:-70px; bottom:-95px; border-radius:50%; background:rgba(217,139,41,.32)}
    .scenario h2{font-family:"Iowan Old Style","Palatino",serif; font-size:25px; margin:0 0 12px}
    .scenario p{margin:0; color:rgba(255,248,232,.78); line-height:1.55; position:relative; z-index:1}
    .actions{display:grid; gap:12px; margin-top:22px}
    button,a.button{border:0; border-radius:18px; padding:15px 18px; font-weight:900; font-size:15px; cursor:pointer; text-align:center; text-decoration:none; transition:.16s ease}
    button:hover,a.button:hover{transform:translateY(-2px)} button:disabled{opacity:.62; transform:none; cursor:wait}
    .primary{color:#fffaf0; background:linear-gradient(135deg,var(--amber),#b96025); box-shadow:0 16px 30px rgba(217,139,41,.3)}
    .secondary{color:var(--pine); background:rgba(255,255,255,.58); border:1px solid var(--line)}
    .grid{display:grid; grid-template-columns:.95fr 1.05fr; gap:22px; margin-top:24px}
    .panel{border-radius:30px; padding:26px; animation:rise .7s ease both .12s}
    .title{margin-bottom:18px}.title h2{font-family:"Iowan Old Style","Palatino",serif; font-size:34px; letter-spacing:-.035em; margin:0}.title p{margin:5px 0 0; color:var(--muted); line-height:1.45}
    .flow{display:grid; gap:14px}.step{border-color:var(--line); border-radius:24px; padding:18px; display:grid; grid-template-columns:44px 1fr auto; gap:14px; align-items:center; box-shadow:0 16px 36px rgba(23,63,54,.11)}
    .num{width:44px;height:44px;border-radius:16px;display:grid;place-items:center;background:var(--pine);color:#fffaf0;font-weight:900}.step h3{margin:0;font-size:17px}.step p{margin:4px 0 0;color:var(--muted);font-size:14px;line-height:1.45}
    .status{border-radius:999px; padding:7px 10px; font-size:12px; font-weight:900; text-transform:uppercase; background:rgba(99,112,107,.12); color:var(--muted)}.status.done{color:#214f36;background:rgba(113,143,63,.18)}.status.fail{color:#8e3227;background:rgba(215,92,71,.16)}
    pre{margin-top:16px; border-radius:22px; padding:16px; background:rgba(23,33,31,.92); color:#f6eddc; overflow:auto; max-height:255px; font:12px/1.55 "SFMono-Regular",Menlo,monospace; white-space:pre-wrap}
    .decisions{display:grid; grid-template-columns:repeat(2,1fr); gap:14px}.decision{border-radius:24px; padding:18px; min-height:150px; border-color:var(--line); box-shadow:none; position:relative; overflow:hidden}.decision:before{content:"";position:absolute;inset:0 auto 0 0;width:7px;background:var(--muted)}.decision.allow:before{background:var(--moss)}.decision.deny:before{background:var(--coral)}
    .decision h3{margin:0 0 12px}.pill{display:inline-flex;border-radius:999px;padding:8px 11px;font-size:12px;font-weight:900;text-transform:uppercase;letter-spacing:.05em}.pill.allow{color:#214d2b;background:rgba(113,143,63,.2)}.pill.deny{color:#8e3227;background:rgba(215,92,71,.17)}
    .reason{margin-top:13px;color:var(--muted);font-size:14px;line-height:1.45}.audit{display:grid;gap:10px}.audit-row{display:grid;grid-template-columns:auto 1fr auto;gap:12px;align-items:center;padding:12px;border:1px solid var(--line);border-radius:18px;background:rgba(255,255,255,.46)}.audit-row strong{display:block;font-size:13px}.audit-row span{color:var(--muted);font-size:12px}
    .empty{border:1px dashed var(--line); border-radius:20px; padding:18px; color:var(--muted); line-height:1.5}
    .toast{position:fixed;left:50%;bottom:24px;transform:translateX(-50%) translateY(18px);opacity:0;padding:13px 17px;border-radius:999px;color:#fffaf0;background:rgba(23,33,31,.92);box-shadow:0 16px 40px rgba(23,33,31,.25);transition:.18s ease;z-index:20}.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
    @keyframes rise{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}
    @media(max-width:920px){.hero,.grid{grid-template-columns:1fr}.metrics,.decisions{grid-template-columns:1fr}.card{padding:30px}.step{grid-template-columns:40px 1fr}.step .status{grid-column:2;justify-self:start}}
  </style>
</head>
<body>
  <main class="shell">
    <section class="hero">
      <div class="card">
        <div class="eyebrow"><span class="dot"></span> Agent Authorization Layer</div>
        <h1>Let AI agents call your API safely.</h1>
        <p class="lead">TrustMesh turns an agent request into a clear authorization decision: who the agent is, who authorized it, what it can do, and why a request is allowed or denied.</p>
        <div class="metrics">
          <div class="metric"><strong>Identity</strong><span>Register agents with did:key identities.</span></div>
          <div class="metric"><strong>Scope</strong><span>Issue credentials with action and resource limits.</span></div>
          <div class="metric"><strong>Audit</strong><span>Record every allow and deny decision.</span></div>
        </div>
      </div>
      <aside class="card control">
        <div class="scenario"><h2>Procurement Agent Demo</h2><p>Alice Corp's AI procurement agent may call Acme's API only for vendor acme, only for purchase.create, and only under $500.</p></div>
        <div class="actions">
          <button id="run" class="primary">Run full authorization demo</button>
          <button id="reset" class="secondary">Reset screen</button>
          <a class="button secondary" href="/docs" target="_blank">Open API docs</a>
        </div>
      </aside>
    </section>
    <section class="grid">
      <div class="panel">
        <div class="title"><h2>Flow</h2><p>Four steps turn a raw agent request into a decision.</p></div>
        <div class="flow">
          <div class="step" data-step="agent"><div class="num">1</div><div><h3>Register agent</h3><p>Create a did:key identity and Ed25519 keypair.</p></div><div class="status">Waiting</div></div>
          <div class="step" data-step="credential"><div class="num">2</div><div><h3>Issue credential</h3><p>Grant audience, action, resource, and amount scope.</p></div><div class="status">Waiting</div></div>
          <div class="step" data-step="verify"><div class="num">3</div><div><h3>Verify requests</h3><p>Evaluate valid, wrong vendor, over limit, and forbidden action requests.</p></div><div class="status">Waiting</div></div>
          <div class="step" data-step="audit"><div class="num">4</div><div><h3>Inspect audit trail</h3><p>Show deny logs with reasons and request context.</p></div><div class="status">Waiting</div></div>
        </div>
        <pre id="identity">Run the demo to see generated agent and credential IDs.</pre>
      </div>
      <div class="panel">
        <div class="title"><h2>Decisions</h2><p>Customers immediately see allow, deny, and reason.</p></div>
        <div id="decisions" class="decisions"><div class="empty">No decisions yet. Click "Run full authorization demo".</div></div>
        <div class="title" style="margin-top:24px"><h2>Audit Logs</h2><p>Every verification decision is stored for review.</p></div>
        <div id="audit" class="audit"><div class="empty">Audit logs will appear after verification requests run.</div></div>
      </div>
    </section>
  </main>
  <div id="toast" class="toast"></div>
  <script>
    const runBtn=document.querySelector("#run"), resetBtn=document.querySelector("#reset"), identity=document.querySelector("#identity"), decisions=document.querySelector("#decisions"), audit=document.querySelector("#audit"), toast=document.querySelector("#toast");
    const state={agent:null,credential:null,results:[]};
    function notify(m){toast.textContent=m;toast.classList.add("show");setTimeout(()=>toast.classList.remove("show"),2600)}
    function step(name,text,fail=false){const el=document.querySelector(`[data-step="${name}"] .status`);el.textContent=text;el.classList.toggle("done",!fail&&text!=="Waiting");el.classList.toggle("fail",fail)}
    async function api(path,options={}){const res=await fetch(path,{headers:{"Content-Type":"application/json",...(options.headers||{})},...options});const body=await res.json();if(!res.ok)throw new Error(body.detail||JSON.stringify(body));return body}
    function showIdentity(){identity.textContent=JSON.stringify({agent_id:state.agent.id,agent_did:state.agent.did,credential_id:state.credential.id,granted_scope:state.credential.claims},null,2)}
    function explanation(r){const map={resource_scope_mismatch:"Agent tried to operate on a vendor outside its scope.",amount_limit_exceeded:"Requested amount exceeded the per-operation spending limit.",action_not_allowed:"Requested action was not listed in allowed_actions.",credential_revoked:"Credential was revoked."};return r.allowed?"Request is inside the credential scope.":(map[r.reason]||"TrustMesh denied this request.")}
    function renderDecisions(){decisions.innerHTML=state.results.map(({label,result})=>{const v=result.allowed?"allow":"deny";return `<article class="decision ${v}"><h3>${label}</h3><span class="pill ${v}">${v}</span><div class="reason"><strong>${result.reason||"in_scope"}</strong><br>${explanation(result)}</div></article>`}).join("")}
    function renderAudit(logs){audit.innerHTML=logs.length?logs.map(l=>`<div class="audit-row"><span class="pill ${l.result==="allow"?"allow":"deny"}">${l.result}</span><div><strong>${l.action||"unknown"}</strong><span>${l.reason||"allowed"} · ${JSON.stringify(l.resource||{})}</span></div><span>${new Date(l.verified_at).toLocaleTimeString()}</span></div>`).join(""):`<div class="empty">No logs found yet.</div>`}
    async function runDemo(){runBtn.disabled=true;runBtn.textContent="Running demo...";state.results=[];decisions.innerHTML=`<div class="empty">Running verification checks...</div>`;audit.innerHTML=`<div class="empty">Waiting for audit logs...</div>`;
      try{
        step("agent","Running"); state.agent=await api("/v1/agents",{method:"POST",body:JSON.stringify({name:"Alice Procurement Agent",operator:"alice@alicecorp.com",metadata:{team:"procurement",demo:"customer-ui"}})}); step("agent","Done");
        step("credential","Running"); state.credential=await api("/v1/credentials/issue",{method:"POST",body:JSON.stringify({issuer:state.agent.did,subject:state.agent.did,claims:{authorized_by:"alice@alicecorp.com",audience:"acme-procurement-api",allowed_actions:["purchase.create","catalog.read"],resource_scope:{vendor_id:"acme"},spending_limit_usd:500},expires_in:86400})}); showIdentity(); step("credential","Done");
        step("verify","Running"); const cases=[["Valid purchase",{action:"purchase.create",resource:{vendor_id:"acme"},amount_usd:180}],["Wrong vendor",{action:"purchase.create",resource:{vendor_id:"other-vendor"},amount_usd:180}],["Over limit",{action:"purchase.create",resource:{vendor_id:"acme"},amount_usd:999}],["Forbidden action",{action:"purchase.delete",resource:{vendor_id:"acme"},amount_usd:180}]];
        for(const [label,body] of cases){const result=await api("/v1/credentials/verify",{method:"POST",body:JSON.stringify({jwt:state.credential.jwt,audience:"acme-procurement-api",...body})});state.results.push({label,result})}
        renderDecisions(); step("verify","Done");
        step("audit","Running"); renderAudit(await api("/v1/audit-logs?limit=6")); step("audit","Done"); notify("Demo completed.");
      }catch(e){notify(e.message);["agent","credential","verify","audit"].forEach(s=>{if(document.querySelector(`[data-step="${s}"] .status`).textContent==="Running")step(s,"Failed",true)})}
      finally{runBtn.disabled=false;runBtn.textContent="Run full authorization demo"}
    }
    function reset(){state.agent=null;state.credential=null;state.results=[];["agent","credential","verify","audit"].forEach(s=>step(s,"Waiting"));identity.textContent="Run the demo to see generated agent and credential IDs.";decisions.innerHTML=`<div class="empty">No decisions yet. Click "Run full authorization demo".</div>`;audit.innerHTML=`<div class="empty">Audit logs will appear after verification requests run.</div>`}
    runBtn.addEventListener("click",runDemo); resetBtn.addEventListener("click",reset);
  </script>
</body>
</html>
"""
