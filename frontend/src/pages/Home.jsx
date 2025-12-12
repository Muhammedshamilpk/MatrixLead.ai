import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Send, CheckCircle, Loader2 } from 'lucide-react'
import axios from 'axios'
import { Link } from 'react-router-dom'
import "../index.css"

const API_URL = "http://127.0.0.1:8000/api/leads";


export default function Home() {
  const [form, setForm] = useState({
    name: '',
    email: '',
    phone: '',
    company: '',
    message: ''
  })
  const [status, setStatus] = useState('idle') // idle, loading, success, error

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setStatus('loading')
    try {
      await axios.post(API_URL, {
        name: form.name,
        email: form.email,
        phone: form.phone,
        company: form.company,
        data: { message: form.message }
      })
      setStatus('success')
    } catch (err) {
      console.error(err)
      setStatus('error')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4 lg:p-8 bg-black relative overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0 aurora-bg z-0 opacity-70"></div>
      <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 brightness-100 contrast-150 mix-blend-overlay pointer-events-none z-0"></div>

      {/* Admin Link */}
      <div className="absolute top-4 right-4 z-50">
        <Link to="/dashboard" className="px-4 py-2 rounded-full bg-white/10 hover:bg-white/20 border border-white/10 text-white text-xs font-mono uppercase tracking-widest transition-all backdrop-blur-md flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
          Admin Terminal
        </Link>
      </div>

      <div className="relative w-full max-w-7xl grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-24 items-center z-10">

        {/* Left: Hero */}
        <motion.div
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="order-2 lg:order-1 relative"
        >
          <div className="relative z-10">
            <div className="inline-flex items-center gap-3 px-4 py-2 rounded-full bg-white/5 border border-white/10 mb-8 backdrop-blur-md shadow-lg shadow-black/20">
              <span className="relative flex h-3 w-3">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
              </span>
              <span className="text-xs font-bold tracking-widest uppercase text-gray-300">Neural Link Active</span>
            </div>

            <h1 className="text-5xl lg:text-7xl font-bold leading-tight mb-6 tracking-tight">
              <span className="text-white drop-shadow-2xl">Deploy </span>
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-primary-400 via-accent-cyan to-accent-pink text-glow">
                Autonomous Agents
              </span>
              <span className="text-white">.</span>
            </h1>

            <p className="text-xl text-gray-300 mb-10 max-w-xl leading-relaxed font-light">
              Qualify leads 24/7 with zero human latency. Experience the next evolution of sales automation.
            </p>

            <div className="flex items-center gap-6">
              <div className="flex -space-x-3">
                {[1, 2, 3, 4].map(i => (
                  <div key={i} className="w-10 h-10 rounded-full bg-gradient-to-b from-gray-700 to-black border border-white/20 flex items-center justify-center shadow-lg">
                    <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                  </div>
                ))}
              </div>
              <div className="text-sm font-medium text-gray-400">
                <span className="text-white">4 Agents</span> standing by
              </div>
            </div>
          </div>
        </motion.div>

        {/* Right: Form */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="order-1 lg:order-2"
        >
          <div className="glass-panel p-8 md:p-12 relative">
            <AnimatePresence mode='wait'>
              {status === 'success' ? (
                <motion.div
                  key="success"
                  initial={{ scale: 0.9, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  className="text-center py-16"
                >
                  <div className="relative w-24 h-24 mx-auto mb-8">
                    <div className="absolute inset-0 bg-green-500/20 rounded-full blur-xl animate-pulse"></div>
                    <div className="relative w-full h-full bg-gradient-to-br from-green-500 to-emerald-600 rounded-full flex items-center justify-center shadow-2xl border border-white/20">
                      <CheckCircle className="w-10 h-10 text-white" />
                    </div>
                  </div>

                  <h2 className="text-4xl font-bold text-white mb-4 tracking-tight">Transmission Secured</h2>
                  <p className="text-gray-400 mb-10 text-lg">Agents have begun analysis. Stand by for contact.</p>

                  <button
                    onClick={() => { setStatus('idle'); setForm({ name: '', email: '', phone: '', company: '', message: '' }) }}
                    className="px-8 py-3 rounded-full border border-white/10 bg-white/5 hover:bg-white/10 text-sm font-semibold tracking-widest uppercase transition-all"
                  >
                    Reset Uplink
                  </button>
                </motion.div>
              ) : (
                <motion.form
                  key="form"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0, y: -20 }}
                  onSubmit={handleSubmit}
                  className="space-y-6"
                >
                  <div className="mb-8">
                    <h3 className="text-2xl font-bold text-white mb-2">Initialize Sequence</h3>
                    <div className="h-1 w-12 bg-primary-500 rounded-full"></div>
                  </div>

                  <div className="space-y-5">
                    <div className="grid grid-cols-2 gap-5">
                      <div className="group">
                        <input required name="name" value={form.name} onChange={handleChange} className="input-field" placeholder="Full Name" />
                      </div>
                      <div className="group">
                        <input required name="company" value={form.company} onChange={handleChange} className="input-field" placeholder="Organization" />
                      </div>
                    </div>

                    <div className="group">
                      <input required type="email" name="email" value={form.email} onChange={handleChange} className="input-field" placeholder="Secure Email" />
                    </div>

                    <div className="group">
                      <input name="phone" value={form.phone} onChange={handleChange} className="input-field" placeholder="Comms Frequency (Phone)" />
                    </div>

                    <div className="group">
                      <textarea required name="message" value={form.message} onChange={handleChange} rows="4" className="input-field resize-none" placeholder="Mission Parameters..."></textarea>
                    </div>
                  </div>

                  <button
                    disabled={status === 'loading'}
                    type="submit"
                    className="btn-primary group mt-6"
                  >
                    <div className="relative flex items-center justify-center gap-3">
                      {status === 'loading' ? (
                        <>
                          <Loader2 className="w-5 h-5 animate-spin" />
                          <span className="tracking-widest uppercase text-sm">Uploading...</span>
                        </>
                      ) : (
                        <>
                          <span className="tracking-widest uppercase text-sm">Establish Connection</span>
                          <Send className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                        </>
                      )}
                    </div>
                  </button>

                  {status === 'error' && (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mt-4 p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400 text-center font-medium">
                      Signal Lost. Please retry.
                    </motion.div>
                  )}
                </motion.form>
              )}
            </AnimatePresence>
          </div>
        </motion.div>
      </div>
    </div>
  )
}
