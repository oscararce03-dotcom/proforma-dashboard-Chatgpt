import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, LineChart, Line, CartesianGrid, Legend } from "recharts";
import { Menu, LogOut, RefreshCw, TrendingUp, AlertTriangle, Building2, Target } from "lucide-react";
import "./styles.css";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";
const money = (n:number|undefined|null) => n == null ? "—" : new Intl.NumberFormat("es-CL",{style:"currency",currency:"CLP",maximumFractionDigits:0}).format(n);
const pct = (n:number|undefined|null) => n == null ? "—" : `${n.toLocaleString("es-CL",{maximumFractionDigits:1})}%`;

async function api(path:string, options:any = {}) {
  const token = localStorage.getItem("proforma_token");
  const r = await fetch(`${API}${path}`, { ...options, headers: { "Content-Type":"application/json", ...(token ? {Authorization:`Bearer ${token}`} : {}), ...(options.headers||{}) }});
  if(!r.ok) throw new Error((await r.json().catch(()=>({}))).detail || "Error de conexión");
  return r.json();
}

function Login({onLogin}:{onLogin:()=>void}) {
  const [u,setU]=useState(""); const [p,setP]=useState(""); const [error,setError]=useState("");
  async function submit(e:React.FormEvent){e.preventDefault();setError("");try{const d=await api("/api/auth/login",{method:"POST",body:JSON.stringify({username:u,password:p})});localStorage.setItem("proforma_token",d.access_token);onLogin()}catch(err:any){setError(err.message)}}
  return <div className="login"><form onSubmit={submit} className="login-card">
    <div className="brand">PROFORMA<span> DASHBOARD</span></div><h1>Acceso</h1>
    <input placeholder="Usuario" value={u} onChange={e=>setU(e.target.value)} />
    <input placeholder="Contraseña" type="password" value={p} onChange={e=>setP(e.target.value)} />
    {error&&<div className="error">{error}</div>}<button>Ingresar</button>
  </form></div>
}

function KPI({title,value,icon:Icon,sub}:{title:string,value:string,icon:any,sub?:string}) {
 return <div className="kpi"><div className="kpi-icon"><Icon size={20}/></div><div><div className="muted">{title}</div><div className="kpi-value">{value}</div>{sub&&<small>{sub}</small>}</div></div>
}

function Table({rows}:{rows:any[]}) {
 if(!rows.length) return <div className="empty">No hay información</div>;
 const cols=Object.keys(rows[0]).slice(0,8);
 return <div className="table-wrap"><table><thead><tr>{cols.map(c=><th key={c}>{c}</th>)}</tr></thead><tbody>{rows.slice(0,100).map((r:any,i:number)=><tr key={i}>{cols.map(c=><td key={c}>{r[c] == null ? "—" : typeof r[c]==="number" ? r[c].toLocaleString("es-CL") : String(r[c])}</td>)}</tr>)}</tbody></table></div>
}

function App(){
 const [logged,setLogged]=useState(!!localStorage.getItem("proforma_token"));
 const [page,setPage]=useState("resumen"); const [open,setOpen]=useState(false);
 const [aportes,setAportes]=useState<any>(null); const [oport,setOport]=useState<any>(null); const [general,setGeneral]=useState<any>(null);
 const [holding,setHolding]=useState(""); const [ej,setEj]=useState(""); const [zona,setZona]=useState("");
 const nav=[["resumen","Resumen Ejecutivo"],["validacion","Validación Excel"],["qa","Control Excel vs BI"],["objetivo","Objetivo 2026"],["comparativos","Comparativos"],["detalle","Detalle Gerencial"],["comparativo","Comp 2025-2026"],["parcial","Comp PP 2025-2026"],["aportes","Comp Aportes"],["8020","Análisis 80/20"],["oportunidad","Oportunidad de Crecimiento"]];
 useEffect(()=>{if(!logged)return;api("/api/general/resumen").then(setGeneral).catch(()=>{});},[logged]);
 useEffect(()=>{if(!logged)return;if(page==="aportes")api(`/api/comercial/aportes?${holding?`holding=${encodeURIComponent(holding)}&`:""}${ej?`ejecutiva=${encodeURIComponent(ej)}`:""}`).then(setAportes);if(page==="oportunidad")api(`/api/comercial/oportunidad?${ej?`ejecutiva=${encodeURIComponent(ej)}&`:""}${zona?`zona=${encodeURIComponent(zona)}`:""}`).then(setOport)},[page,holding,ej,zona,logged]);
 if(!logged)return <Login onLogin={()=>setLogged(true)}/>;
 const logout=()=>{localStorage.removeItem("proforma_token");setLogged(false)};
 const rows=general?.rows||[];
 const content = <>
   {page==="resumen" && <><h1>Resumen Ejecutivo</h1><p className="lead">Visión gerencial de la información del Cuadro de Mando.</p><div className="kpis"><KPI title="Registros" value={rows.length.toLocaleString("es-CL")} icon={Building2}/><KPI title="Estado" value="Operativo" icon={TrendingUp}/><KPI title="Fuente" value="Excel XLSM" icon={Target}/><KPI title="Alertas" value="Derivadas de datos" icon={AlertTriangle}/></div><section className="card"><h2>Cuadro de Mando</h2><Table rows={rows.slice(0,20)}/></section></>}
   {page==="objetivo" && <DataPage title="Objetivo 2026" endpoint="/api/general/objetivo"/>}
   {page==="comparativos" && <DataPage title="Comparativos" endpoint="/api/general/comparativos"/>}
   {page==="detalle" && <DataPage title="Detalle Gerencial" endpoint="/api/general/detalle"/>}
   {page==="comparativo" && <DataPage title="Comp 2025-2026" endpoint="/api/comercial/comparativo" chart/>}
   {page==="parcial" && <DataPage title="Comp PP 2025-2026" endpoint="/api/comercial/comparativo-parcial"/>}
   {page==="8020" && <Pareto/>}
   {page==="aportes" && <><h1>Comp Aportes</h1><Filters type="aportes" holding={holding} setHolding={setHolding} ej={ej} setEj={setEj} zona={zona} setZona={setZona} data={aportes}/><div className="kpis">{["aporte_total_2025","aporte_parcial_2025","aporte_parcial_2026","diferencia"].map((k)=><KPI key={k} title={k.replaceAll("_"," ")} value={money(aportes?.metrics?.[k])} icon={TrendingUp}/>)}</div><section className="card"><Table rows={aportes?.rows||[]}/></section></>}
   {page==="oportunidad" && <><h1>Oportunidad de Crecimiento</h1><Filters type="oportunidad" holding={holding} setHolding={setHolding} ej={ej} setEj={setEj} zona={zona} setZona={setZona} data={oport}/><div className="kpis">{([["aporte_actual","Aporte actual"],["potencial","Potencial"],["oportunidad","Oportunidad"],["empresas","Empresas"]] as [string,string][]).map(([k,t])=><KPI key={k} title={t} value={k==="empresas"?String(oport?.metrics?.[k]??"—"):money(oport?.metrics?.[k])} icon={Target}/>)}</div><section className="card"><Table rows={oport?.rows||[]}/></section></>}
 </>;
 return <div className="shell"><aside className={open?"sidebar open":"sidebar"}><div className="brand">PROFORMA</div><div className="section-label">DASHBOARD</div>{nav.map(([id,label])=><button key={id} className={page===id?"nav active":"nav"} onClick={()=>{setPage(id);setOpen(false)}}>{label}</button>)}</aside><main><header><button className="menu" onClick={()=>setOpen(!open)}><Menu/></button><div><strong>PROFORMA DASHBOARD</strong><span> Business Intelligence</span></div><div className="header-right"><button className="icon-btn" onClick={()=>location.reload()} title="Actualizar"><RefreshCw size={18}/></button><button className="logout" onClick={logout}><LogOut size={17}/> Salir</button></div></header><div className="content">{content}</div></main></div>
}

function DataPage({title,endpoint,chart=false}:{title:string,endpoint:string,chart?:boolean}){const [d,setD]=useState<any>(null);useEffect(()=>{api(endpoint).then(setD).catch(()=>{})},[endpoint]);const rows=d?.rows||d?.cuadro_1||[];const chartData=rows.slice(0,12).map((r:any,i:number)=>({name:String(Object.values(r)[0]??i+1).slice(0,18),value:Number(Object.values(r).find(v=>typeof v==="number")||0)}));return <><h1>{title}</h1><section className="card">{chart&&<div className="chart"><ResponsiveContainer width="100%" height={300}><BarChart data={chartData}><CartesianGrid strokeDasharray="3 3"/><XAxis dataKey="name"/><YAxis/><Tooltip/><Bar dataKey="value" fill="#F28C28"/></BarChart></ResponsiveContainer></div>}<Table rows={rows}/></section></>}

function Filters({type,holding,setHolding,ej,setEj,zona,setZona,data}:{type:string,holding:string,setHolding:any,ej:string,setEj:any,zona:string,setZona:any,data:any}){return <div className="filters"><select value={type==="aportes"?holding:ej} onChange={e=>type==="aportes"?setHolding(e.target.value):setEj(e.target.value)}><option value="">Todos</option>{(type==="aportes"?data?.holdings:data?.ejecutivas||[]).map((x:string)=><option key={x}>{x}</option>)}</select>{type==="aportes"?<select value={ej} onChange={e=>setEj(e.target.value)}><option value="">Todas las ejecutivas</option>{(data?.ejecutivas||[]).map((x:string)=><option key={x}>{x}</option>)}</select>:<select value={zona} onChange={e=>setZona(e.target.value)}><option value="">Todas las zonas</option>{(data?.zonas||[]).map((x:string)=><option key={x}>{x}</option>)}</select>}<button onClick={()=>{setHolding("");setEj("");setZona("")}}>Limpiar filtros</button></div>}

function Pareto(){const [d,setD]=useState<any>(null);useEffect(()=>{api("/api/comercial/80-20").then(setD).catch(()=>{})},[]);const rows=(d?.rows||[]).filter((r:any)=>r.Holding);const chartRows=rows.map((r:any)=>({name:String(r.Holding).slice(0,16),aporte:Number(r["2025"]||0)}));const total=chartRows.reduce((a:any,b:any)=>a+b.aporte,0);let acc=0;const pareto=chartRows.map((r:any)=>{acc+=r.aporte;return {...r,acumulado:total?acc/total*100:0}});return <><h1>Análisis 80/20</h1><p className="lead">Concentración de aportes por Holding.</p><div className="kpis"><KPI title="Aporte total 2025" value={money(total)} icon={Target}/><KPI title="Nº Holdings" value={String(rows.length)} icon={Building2}/><KPI title="Top 5" value={money(pareto.slice(0,5).reduce((a:any,b:any)=>a+b.aporte,0))} icon={TrendingUp}/><KPI title="Concentración Top 10" value={pct(total?pareto.slice(0,10).reduce((a:any,b:any)=>a+b.aporte,0)/total*100:null)} icon={AlertTriangle}/></div><section className="card"><h2>Gráfico de Pareto</h2><div className="chart"><ResponsiveContainer width="100%" height={380}><LineChart data={pareto.slice(0,25)}><CartesianGrid strokeDasharray="3 3"/><XAxis dataKey="name"/><YAxis yAxisId="left"/><YAxis yAxisId="right" orientation="right" domain={[0,100]}/><Tooltip formatter={(v:any,n:any)=>n==="acumulado"?pct(v):money(v)}/><Legend/><Bar yAxisId="left" dataKey="aporte" fill="#F28C28" name="Aporte 2025"/><Line yAxisId="right" type="monotone" dataKey="acumulado" stroke="#333333" name="% acumulado"/></LineChart></ResponsiveContainer></div><Table rows={rows}/></section></>}

function QAPage(){const[d,setD]=useState<any>(null);useEffect(()=>{api("/api/admin/qa").then(setD).catch(()=>{})},[]);return <><h1>Control Excel vs BI</h1><p className="lead">Validación independiente de la fuente XLSM y de los totales críticos.</p><div className="card"><div className="qa-banner"><b>{d?.status==="OK"?"✓ VALIDACIÓN OK":d?.status==="WARNING"?"⚠ REVISAR ADVERTENCIAS":d?.status==="ERROR"?"✕ ERROR":"Validando…"}</b><span>{d?.checks??"—"} controles · {d?.errors??"—"} errores · {d?.warnings??"—"} advertencias</span></div></div><section className="card"><h2>Conciliación independiente</h2><Table rows={(d?.checks_detail||[]).filter((x:any)=>x.type==="independent_total")}/></section></>}

createRoot(document.getElementById("root")!).render(<App/>);
