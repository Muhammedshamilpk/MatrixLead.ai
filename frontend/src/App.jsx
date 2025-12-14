import { BrowserRouter, Routes, Route } from "react-router-dom"
import Home from "./pages/Home"
import Dashboard from "./pages/Dashboard"
import LeadQualificationForm from "./pages/LeadQualificationForm"
import ErrorBoundary from "./ErrorBoundary"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />

        <Route path="/qualify" element={<LeadQualificationForm />} />

        <Route
          path="/dashboard"
          element={
            <ErrorBoundary>
              <Dashboard />
            </ErrorBoundary>
          }
        />
      </Routes>
    </BrowserRouter>
  )
}

export default App
