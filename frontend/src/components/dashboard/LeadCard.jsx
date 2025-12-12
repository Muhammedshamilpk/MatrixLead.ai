import { motion } from "framer-motion"
import { ExternalLink } from "lucide-react"

export default function LeadCard({ lead, index, onView }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      className="bg-zinc-900/40 p-6 rounded-2xl border border-white/5 hover:border-green-500/30 transition"
    >
      <div className="flex justify-between">
        <div>
          <h3 className="text-lg font-bold">{lead.name}</h3>
          <p className="text-sm text-gray-400">{lead.email}</p>
        </div>

        <div className="text-right">
          <span className="text-xl font-bold">{(lead.score * 100).toFixed(0)}%</span>
          <div className="text-[10px] text-gray-500">Match</div>
        </div>
      </div>

      <button
        onClick={onView}
        className="mt-4 px-3 py-1.5 bg-white/10 rounded-md text-xs font-bold uppercase tracking-widest hover:bg-white/20"
      >
        View Data <ExternalLink className="inline ml-1 w-3 h-3" />
      </button>
    </motion.div>
  )
}
