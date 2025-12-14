import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { ArrowRight } from 'lucide-react'
import "../index.css"

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 relative overflow-hidden bg-black selection:bg-primary-500/30">
      {/* Background Elements */}
      <div className="absolute inset-0 aurora-bg z-0 opacity-60"></div>
      <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 brightness-100 contrast-150 mix-blend-overlay pointer-events-none z-0"></div>

      <div className="relative z-10 text-center max-w-5xl px-4">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="flex flex-col items-center"
        >


          {/* Main Heading */}
          <h1 className="text-6xl md:text-8xl lg:text-9xl font-black tracking-tighter mb-6 relative z-20">
            <span className="bg-clip-text text-transparent bg-gradient-to-br from-white via-gray-200 to-gray-500 drop-shadow-2xl">
              Matrix
            </span>
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-primary-400 via-accent-cyan to-accent-pink text-glow">
              Lead
            </span>
          </h1>

          {/* Subtitle */}
          <p className="text-xl md:text-2xl text-gray-400 mb-12 max-w-3xl font-light leading-relaxed">
            Let AI qualify your leads for you.
          </p>

          {/* CTA Button */}
          <Link
            to="/qualify"
            className="group relative inline-flex items-center gap-3 px-8 py-4 bg-white/5 border border-white/20 hover:bg-white/10 rounded-full backdrop-blur-sm transition-all duration-300 hover:scale-105 hover:shadow-[0_0_40px_rgba(255,255,255,0.1)]"
          >
            <span className="text-white font-bold tracking-wide uppercase text-sm">Start</span>
            <ArrowRight className="w-5 h-5 text-accent-cyan group-hover:translate-x-1 transition-transform" />

            {/* Button Glow Effect */}
            <div className="absolute inset-0 rounded-full ring-1 ring-white/20 group-hover:ring-white/40 transition-all"></div>
          </Link>
        </motion.div>
      </div>

      {/* Footer */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1, duration: 1 }}
        className="absolute bottom-8 w-full text-center"
      >
        <p className="text-white/30 text-xs font-mono tracking-[0.2em] uppercase">
          MatrixLead AI © 2025 // Secure Connection
        </p>
      </motion.div>
    </div>
  )
}
