import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
  LayoutDashboard,
  MessageSquare,
  Mail,
  CheckCircle,
  Settings,
  Search,
  User,
  Zap,
  Activity,
  X,
} from "lucide-react";
import axios from "axios";
import "../index.css";

const API_URL = "http://127.0.0.1:8000/api/leads";


export default function Dashboard() {
  const [activeTab, setActiveTab] = useState("home");
  const [leads, setLeads] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedLead, setSelectedLead] = useState(null);

  useEffect(() => {
    fetchLeads();
  }, []);

  const fetchLeads = async () => {
    try {
      console.log("📡 Fetching leads from:", API_URL);
      const res = await axios.get(API_URL);
      console.log("✅ API response:", res.data);
      setLeads(Array.isArray(res.data) ? res.data : []);
    } catch (err) {
      console.error("🔥 ERROR fetching leads:", err);
      setLeads([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white flex overflow-hidden">

      {/* SIDEBAR */}
      <div className="w-72 bg-zinc-900/40 border-r border-white/5 p-6 space-y-4">
        <h1 className="text-2xl font-bold flex items-center gap-2">
          Matrix <span className="text-green-400">Lead</span>
        </h1>

        <NavItem icon={LayoutDashboard} label="Home" active={activeTab === "home"} onClick={() => setActiveTab("home")} />
        <NavItem icon={User} label="All Leads" active={activeTab === "leads"} onClick={() => setActiveTab("leads")} />
        <NavItem icon={Mail} label="Email" active={activeTab === "email"} onClick={() => setActiveTab("email")} />
        <NavItem icon={MessageSquare} label="Chat" active={activeTab === "chat"} onClick={() => setActiveTab("chat")} />
        <NavItem icon={Settings} label="Settings" active={activeTab === "settings"} onClick={() => setActiveTab("settings")} />
      </div>

      {/* MAIN CONTENT */}
      <div className="flex-1 p-8 space-y-6">

        {/* HEADER */}
        <div className="flex justify-between items-center">
          <h2 className="text-3xl font-bold capitalize">{activeTab}</h2>

          <div className="relative">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" />
            <input
              className="bg-zinc-900 border border-white/10 rounded-xl pl-10 pr-4 py-2 text-sm w-64 text-gray-300"
              placeholder="Search..."
            />
          </div>
        </div>

        {/* HOME TAB – STATS */}
        {activeTab === "home" && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">

            <StatCard label="Total Signals" value={leads.length} icon={Activity} color="blue" />

            <StatCard
              label="Active Intercepts"
              value={leads.filter((l) => l.status === "IN_PROGRESS").length}
              icon={MessageSquare}
              color="yellow"
            />

            <StatCard
              label="Qualified Targets"
              value={leads.filter((l) => l.status === "QUALIFIED").length}
              icon={CheckCircle}
              color="green"
            />

            <StatCard label="Response Time" value="1.2s" icon={Zap} color="purple" />
          </div>
        )}

        {/* ALL LEADS */}
        {activeTab === "leads" && (
          loading ? (
            <p className="text-gray-400">Loading...</p>
          ) : leads.length === 0 ? (
            <p className="text-gray-500">No leads found.</p>
          ) : (
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
              {leads.map((lead, idx) => (
                <LeadCard
                  key={idx}
                  index={idx}
                  lead={lead}
                  onClick={() => setSelectedLead(lead)}
                />
              ))}
            </div>
          )
        )}

        {/* EMAIL TAB */}
        {activeTab === "email" && (
          leads.filter((l) => l.email).length === 0 ? (
            <p className="text-gray-500">No emails available.</p>
          ) : (
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
              {leads
                .filter((l) => l.email)
                .map((lead, idx) => (
                  <LeadCard
                    key={idx}
                    index={idx}
                    lead={lead}
                    onClick={() => setSelectedLead(lead)}
                  />
                ))}
            </div>
          )
        )}

        {/* CHAT TAB */}
        {activeTab === "chat" && (
          leads.filter((l) => l.messages?.some((m) => m.type === "chat")).length === 0 ? (
            <p className="text-gray-500">No chat conversations yet.</p>
          ) : (
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
              {leads
                .filter((l) => l.messages?.some((m) => m.type === "chat"))
                .map((lead, idx) => (
                  <LeadCard
                    key={idx}
                    index={idx}
                    lead={lead}
                    onClick={() => setSelectedLead(lead)}
                  />
                ))}
            </div>
          )
        )}
      </div>

      {/* LEAD DETAILS MODAL */}
      <LeadModal lead={selectedLead} onClose={() => setSelectedLead(null)} />
    </div>
  );
}

/* -------------------- COMPONENTS -------------------- */

function NavItem({ icon: Icon, label, active, onClick }) {
  return (
    <button
      onClick={onClick}
      className={`w-full flex items-center px-4 py-3 rounded-xl gap-3
      ${active ? "bg-green-500/20 text-green-400 border border-green-500/20" : "text-gray-400 hover:bg-white/10"}`}
    >
      <Icon className="w-5 h-5" />
      {label}
    </button>
  );
}

function StatCard({ label, value, icon: Icon, color }) {
  const colors = {
    blue: "text-blue-400",
    green: "text-green-400",
    yellow: "text-yellow-400",
    purple: "text-purple-400",
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-zinc-900/40 p-5 rounded-2xl border border-white/5"
    >
      <div className="flex justify-between">
        <Icon className={`w-6 h-6 ${colors[color]}`} />
        <span className="text-sm text-gray-400">{label}</span>
      </div>
      <div className="text-3xl font-bold mt-2">{value}</div>
    </motion.div>
  );
}

function LeadCard({ lead, index, onClick }) {
  return (
    <motion.div
      onClick={onClick}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-zinc-900/40 p-6 rounded-2xl border border-white/5 hover:border-green-500/40 transition cursor-pointer"
    >
      <h3 className="text-xl font-bold">{lead.name}</h3>
      <p className="text-gray-400">{lead.email}</p>

      <div className="mt-4 text-sm">
        <span className="text-gray-500">Status: </span>
        <span className="text-green-400">{lead.status}</span>
      </div>
    </motion.div>
  );
}

function LeadModal({ lead, onClose }) {
  if (!lead) return null;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="fixed inset-0 bg-black/80 flex items-center justify-center p-6 z-50"
    >
      <div className="bg-zinc-900/70 border border-white/10 p-8 rounded-2xl max-w-3xl w-full relative">

        <button onClick={onClose} className="absolute right-4 top-4 text-gray-400 hover:text-white">
          <X className="w-6 h-6" />
        </button>

        <h2 className="text-3xl font-bold mb-6">{lead.name}</h2>

        <InfoRow label="Email" value={lead.email} />
        <InfoRow label="Phone" value={lead.phone} />
        <InfoRow label="Company" value={lead.company} />
        <InfoRow label="Status" value={lead.status} />
        <InfoRow label="Score" value={(lead.score * 100).toFixed(1) + "%"} />

        <p className="text-gray-400 mt-4 mb-2">Raw JSON Data</p>
        <pre className="bg-black/40 p-4 rounded-xl text-gray-300 text-sm max-h-64 overflow-auto">
{JSON.stringify(lead, null, 2)}
        </pre>

      </div>
    </motion.div>
  );
}

function InfoRow({ label, value }) {
  return (
    <div className="flex justify-between text-sm mb-3">
      <span className="text-gray-500">{label}:</span>
      <span className="text-white">{value || "—"}</span>
    </div>
  );
}
