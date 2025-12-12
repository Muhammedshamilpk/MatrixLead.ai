import { motion } from "framer-motion"

export default function NavItem({ icon: Icon, label, active, onClick, badge }) {
  return (
    <button
      onClick={onClick}
      className={`w-full flex items-center justify-between px-4 py-3.5 rounded-xl
        ${active ? "bg-green-500/10 text-green-400 border-l-2 border-green-500"
                : "text-gray-400 hover:bg-white/5"}`}
    >
      <div className="flex items-center gap-3">
        <Icon className="w-5 h-5" />
        <span>{label}</span>
      </div>

      {badge > 0 && (
        <span className="px-2 py-1 text-[10px] bg-green-500/20 text-green-400 rounded-full">
          {badge}
        </span>
      )}
    </button>
  )
}
