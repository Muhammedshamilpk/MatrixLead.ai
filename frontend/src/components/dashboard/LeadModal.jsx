// import { motion } from "framer-motion"
// import { X } from "lucide-react"

// export default function LeadModal({ lead, onClose }) {
//   if (!lead) return null

//   return (
//     <motion.div
//       initial={{ opacity: 0 }}
//       animate={{ opacity: 1 }}
//       className="fixed inset-0 bg-black/80 backdrop-blur-xl flex items-center justify-center z-50 p-6"
//     >
//       <div className="bg-zinc-900/70 border border-white/10 rounded-2xl p-8 w-full max-w-3xl relative">

//         <button onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-white">
//           <X className="w-6 h-6" />
//         </button>

//         <h2 className="text-3xl font-bold mb-6">{lead.name}</h2>

//         <div className="space-y-4">
//           <Info label="Email" value={lead.email} />
//           <Info label="Phone" value={lead.phone} />
//           <Info label="Company" value={lead.company} />
//           <Info label="Status" value={lead.status} />
//           <Info label="Score" value={(lead.score * 100).toFixed(1) + "%"} />

//           <div>
//             <p className="text-gray-400 text-sm mb-2">Raw JSON Data</p>
//             <pre className="bg-black/40 border border-white/10 p-4 rounded-xl text-sm text-gray-300 max-h-64 overflow-auto">
//               {JSON.stringify(lead, null, 2)}
//             </pre>
//           </div>
//         </div>
//       </div>
//     </motion.div>
//   )
// }

// function Info({ label, value }) {
//   return (
//     <div className="flex justify-between text-sm">
//       <span className="text-gray-500">{label}:</span>
//       <span className="text-white">{value || "—"}</span>
//     </div>
//   )
// }

import { motion } from "framer-motion"
import { X } from "lucide-react"

export default function LeadModal({ lead, onClose }) {
  if (!lead) return null

  const statusColor =
    lead.status === "QUALIFIED"
      ? "text-green-400"
      : lead.status === "IN_PROGRESS"
      ? "text-yellow-400"
      : "text-red-400"

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="fixed inset-0 bg-black/80 backdrop-blur-xl flex items-center justify-center z-50 p-6"
    >
      <div className="bg-zinc-900/70 border border-white/10 rounded-2xl p-8 w-full max-w-2xl relative shadow-xl">

        {/* Close Button */}
        <button onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-white">
          <X className="w-6 h-6" />
        </button>

        {/* HEADER */}
        <h2 className="text-3xl font-bold mb-3 capitalize">{lead.name}</h2>
        <p className="text-gray-400">{lead.email}</p>
        <p className="text-gray-400 mb-6">{lead.phone}</p>
        <p className="text-gray-300 mb-6">{lead.company}</p>

        {/* STATUS + SCORE */}
        <div className="flex justify-between items-center mb-6">
          <span className={`text-lg font-semibold ${statusColor}`}>{lead.status}</span>
          <span className="text-white bg-white/10 px-4 py-2 rounded-xl font-bold">
            {(lead.score * 100).toFixed(1)}%
          </span>
        </div>

        {/* AI SIGNALS */}
        <h3 className="text-xl font-semibold text-white mb-3">AI Analysis</h3>

        <div className="space-y-3 text-gray-300">

          <Signal label="Email Type" value={lead.email_type || "—"} />
          <Signal label="Email Score" value={lead.email_score || "—"} />

          <Signal label="Phone Valid" value={lead.phone_valid ? "Yes" : "No"} />
          <Signal label="Phone Region" value={lead.phone_region || "—"} />

          <Signal label="Intent" value={lead.intent || "—"} />
          <Signal label="Spam Probability" value={lead.spam_probability || "—"} />

          <Signal label="Company Status" value={lead.company_status || "—"} />
          <Signal label="Industry" value={lead.company_industry || "—"} />
        </div>

      </div>
    </motion.div>
  )
}

function Signal({ label, value }) {
  return (
    <div className="flex justify-between text-sm border-b border-white/5 pb-2">
      <span className="text-gray-500">{label}</span>
      <span className="text-white font-medium">{value}</span>
    </div>
  )
}
