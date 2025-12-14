import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const LeadQualificationForm = () => {
    const navigate = useNavigate();
    const [currentStep, setCurrentStep] = useState(1);

    // Comprehensive Real-World B2B Data
    const [formData, setFormData] = useState({
        // Step 1: Contact
        name: '',
        jobTitle: '',
        email: '',
        phone: '',
        company: '',

        // Step 2: Org Details
        companySize: '',
        industry: '',
        website: '',

        // Step 3: Qualification (The "Real" Questions)
        authority: '', // Decision making power
        budget: '',
        timeline: '',
        currentSolution: '',
        painPoints: [],
        message: ''
    });

    const [isSubmitting, setIsSubmitting] = useState(false);
    const [result, setResult] = useState(null);

    // --- Configuration: Real World B2B Questions ---
    const questions = {
        step1: {
            title: "Join With Us",
            subtitle: "Fill in the form below to get started",
            fields: [
                { name: 'name', label: 'Full Name', type: 'text', required: true, placeholder: 'Jane Doe' },
                { name: 'jobTitle', label: 'Job Title', type: 'text', required: true, placeholder: 'VP of Marketing' },
                { name: 'email', label: 'Work Email', type: 'email', required: true, placeholder: 'jane@company.com' },
                { name: 'phone', label: 'Phone Number', type: 'tel', required: true, placeholder: '+1 (555) 000-0000' },
                { name: 'company', label: 'Company Name', type: 'text', required: true, placeholder: 'Acme Enterprises' },
                { name: 'website', label: 'Company Website', type: 'text', required: false, placeholder: 'www.acme.com' },
            ]
        },
        step2: {
            title: "Organization Profile",
            subtitle: "Tell us about your company structure",
            fields: [
                {
                    name: 'companySize',
                    label: 'Company Size',
                    type: 'select',
                    required: true,
                    options: [
                        { value: '', label: 'Select employee count' },
                        { value: '1-10', label: '1-10 (Startup)' },
                        { value: '11-50', label: '11-50 (Small Business)' },
                        { value: '51-200', label: '51-200 (Mid-Market)' },
                        { value: '201-1000', label: '201-1,000 (Growth)' },
                        { value: '1000+', label: '1,000+ (Enterprise)' },
                    ]
                },
                {
                    name: 'industry',
                    label: 'Industry',
                    type: 'select',
                    required: true,
                    options: [
                        { value: '', label: 'Select industry' },
                        { value: 'SaaS', label: 'SaaS / Software' },
                        { value: 'Fintech', label: 'Finance / Fintech' },
                        { value: 'Healthcare', label: 'Healthcare / MedTech' },
                        { value: 'E-commerce', label: 'E-commerce / Retail' },
                        { value: 'Manufacturing', label: 'Manufacturing' },
                        { value: 'Consulting', label: 'Consulting / Agency' },
                        { value: 'Education', label: 'Education' },
                        { value: 'Other', label: 'Other' },
                    ]
                },
                {
                    name: 'authority',
                    label: 'What is your role in the purchasing process?',
                    type: 'select',
                    required: true,
                    options: [
                        { value: '', label: 'Select your role' },
                        { value: 'Decision Maker', label: 'I am the sole Decision Maker' },
                        { value: 'Influencer', label: 'I influence the decision (Researcher)' },
                        { value: 'Champion', label: 'I am the internal Champion' },
                        { value: 'End User', label: 'I am an End User' },
                        { value: 'Gatekeeper', label: 'I am gathering info for someone else' },
                    ]
                }
            ]
        },
        step3: {
            title: "Project Scope",
            subtitle: "Help us understand your specific needs",
            fields: [
                {
                    name: 'budget',
                    label: 'What is your estimated budget?',
                    type: 'select',
                    required: true,
                    options: [
                        { value: '', label: 'Select budget range' },
                        { value: 'No Budget', label: 'No budget approved yet' },
                        { value: '< $10k', label: 'Under $10,000' },
                        { value: '$10k-50k', label: '$10,000 - $50,000' },
                        { value: '$50k-100k', label: '$50,000 - $100,000' },
                        { value: '$100k+', label: '$100,000+' },
                    ]
                },
                {
                    name: 'timeline',
                    label: 'When are you looking to implement?',
                    type: 'select',
                    required: true,
                    options: [
                        { value: '', label: 'Select timeline' },
                        { value: 'ASAP', label: 'Immediately (ASAP)' },
                        { value: '1-3 Months', label: 'Within 1-3 Months' },
                        { value: '3-6 Months', label: '3-6 Months' },
                        { value: '6+ Months', label: '6+ Months' },
                        { value: 'Just Browsing', label: 'Just browsing / exploring' },
                    ]
                },
                {
                    name: 'painPoints',
                    label: 'What are your top challenges? (Select all that apply)',
                    type: 'checkbox',
                    required: true,
                    options: [
                        { value: 'Inefficiency', label: 'Team Inefficiency' },
                        { value: 'High Costs', label: 'High Operational Costs' },
                        { value: 'Low Conversion', label: 'Low Lead Conversion' },
                        { value: 'Poor Data', label: 'Poor Data Quality' },
                        { value: 'Scaling Issues', label: 'Difficulty Scaling' },
                        { value: 'Automation', label: 'Need for Automation' },
                    ]
                },
                {
                    name: 'message',
                    label: 'Anything else we should know?',
                    type: 'textarea',
                    required: false,
                    placeholder: 'Specific requirements, questions, or context...',
                }
            ]
        }
    };

    const totalSteps = Object.keys(questions).length;

    const handleInputChange = (e) => {
        const { name, value, type, checked } = e.target;

        if (type === 'checkbox') {
            setFormData(prev => ({
                ...prev,
                [name]: checked
                    ? [...(prev[name] || []), value]
                    : (prev[name] || []).filter(v => v !== value)
            }));
        } else {
            setFormData(prev => ({ ...prev, [name]: value }));
        }
    };

    const handleSubmit = async () => {
        setIsSubmitting(true);

        try {
            // Construct a rich narrative for the AI to analyze
            // This ensures the AI "reads" the real-world qualification data
            const qualificationNarrative = `
Title: ${formData.jobTitle}
Authority Level: ${formData.authority}
Company Size: ${formData.companySize}
Industry: ${formData.industry}
Website: ${formData.website}
Budget: ${formData.budget}
Timeline: ${formData.timeline}
Key Challenges: ${formData.painPoints.join(', ')}

User Message:
${formData.message}
            `.trim();

            const response = await fetch('http://localhost:8000/api/leads', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: formData.name,
                    email: formData.email,
                    phone: formData.phone,
                    company: formData.company,
                    data: {
                        // Pass individual fields for structured data if needed
                        job_title: formData.jobTitle,
                        authority: formData.authority,
                        company_size: formData.companySize,
                        industry: formData.industry,
                        budget: formData.budget,
                        timeline: formData.timeline,
                        pain_points: formData.painPoints,

                        // Pass the narrative to the 'message' field which the AI heavily weights
                        message: qualificationNarrative,
                        source: 'web_qualification_form'
                    }
                })
            });

            if (!response.ok) throw new Error('Failed to submit');
            const lead = await response.json();

            // Poll for the result and logs with retries (up to 10 seconds)
            let updatedLead = lead;
            let emailStatus = false;
            let attempts = 0;
            const maxAttempts = 10;

            while (attempts < maxAttempts) {
                attempts++;

                // 1. Check Lead Status
                const updatedResponse = await fetch(`http://localhost:8000/api/leads`);
                const leads = await updatedResponse.json();
                updatedLead = leads.find(l => l.id === lead.id);

                // 2. Check Logs for Email
                try {
                    const logsResponse = await fetch(`http://localhost:8000/api/leads/${lead.id}/logs`);
                    const logs = await logsResponse.json();

                    const emailLog = logs.find(l =>
                        (l.event === 'auto_email_sent' && l.details?.status === 'sent') ||
                        (l.event === 'manual_email_sent')
                    );

                    if (emailLog) {
                        emailStatus = true;
                        break; // Exit loop if email confirmed
                    }
                } catch (err) {
                    console.warn("Could not fetch logs", err);
                }

                // Wait 1 second before next poll
                await new Promise(resolve => setTimeout(resolve, 1000));
            }

            setResult({
                status: updatedLead?.status || 'RECEIVED',
                score: updatedLead?.score || 0,
                name: formData.name,
                emailSent: emailStatus
            });

        } catch (error) {
            console.error('Error:', error);
            alert('Submission failed. Please try again.');
        } finally {
            setIsSubmitting(false);
        }
    };

    const validateStep = () => {
        const currentQ = questions[`step${currentStep}`];
        return currentQ.fields.every(field => {
            if (!field.required) return true;
            const value = formData[field.name];
            if (field.type === 'checkbox') return value && value.length > 0;
            return value && value.trim() !== '';
        });
    };

    const nextStep = () => {
        if (validateStep()) {
            if (currentStep < totalSteps) setCurrentStep(currentStep + 1);
            else handleSubmit();
        } else {
            alert('Please complete all required fields.');
        }
    };

    const prevStep = () => {
        if (currentStep > 1) setCurrentStep(currentStep - 1);
    };

    // --- Render Logic ---

    if (result) {
        return (
            <div className="min-h-screen bg-black text-white flex items-center justify-center p-6 font-sans">
                <div className="max-w-2xl w-full bg-zinc-900 rounded-3xl border border-zinc-800 p-10 shadow-2xl text-center">
                    <div className="text-6xl mb-6">
                        ✅
                    </div>

                    <h2 className="text-3xl font-bold mb-4 text-white">
                        Application Received
                    </h2>

                    <p className="text-gray-400 mb-8 text-lg leading-relaxed">
                        Thank you for your interest. <br />
                        We have successfully received your details. Our team will review your application and get back to you shortly.
                    </p>

                    {result.emailSent && (
                        <div className="bg-green-900/20 border border-green-900 text-green-400 p-4 rounded-xl mb-8 flex items-center justify-center gap-2">
                            <span className="text-xl">📧</span>
                            <span>A confirmation email has been sent to {formData.email || 'you'}.</span>
                        </div>
                    )}

                    <div className="flex gap-4 justify-center">
                        <button onClick={() => navigate('/dashboard')} className="bg-white text-black px-8 py-3 rounded-xl font-bold hover:bg-gray-200 transition">
                            View Dashboard
                        </button>
                        <button onClick={() => window.location.reload()} className="border border-zinc-700 text-white px-8 py-3 rounded-xl font-bold hover:bg-zinc-800 transition">
                            Submit Another
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    const currentQ = questions[`step${currentStep}`];

    // Helper to render fields
    const renderField = (field) => {
        const commonClasses = "w-full bg-zinc-800 border-zinc-700 rounded-xl px-4 py-3 text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent focus:outline-none transition-all placeholder-gray-500";

        if (field.type === 'select') {
            return (
                <select name={field.name} value={formData[field.name]} onChange={handleInputChange} className={commonClasses}>
                    {field.options.map(opt => <option key={opt.value} value={opt.value}>{opt.label}</option>)}
                </select>
            );
        }
        if (field.type === 'checkbox') {
            return (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {field.options.map(opt => (
                        <label key={opt.value} className={`flex items-center space-x-3 p-3 rounded-lg border cursor-pointer transition-all ${(formData[field.name] || []).includes(opt.value)
                            ? 'bg-purple-900/30 border-purple-500'
                            : 'bg-zinc-800 border-zinc-700 hover:border-zinc-500'
                            }`}>
                            <input
                                type="checkbox"
                                name={field.name}
                                value={opt.value}
                                checked={(formData[field.name] || []).includes(opt.value)}
                                onChange={handleInputChange}
                                className="w-5 h-5 rounded text-purple-600 focus:ring-purple-500 bg-zinc-900 border-zinc-600"
                            />
                            <span className="text-sm">{opt.label}</span>
                        </label>
                    ))}
                </div>
            );
        }
        if (field.type === 'textarea') {
            return <textarea name={field.name} value={formData[field.name]} onChange={handleInputChange} rows={4} placeholder={field.placeholder} className={commonClasses} />;
        }
        return <input type={field.type} name={field.name} value={formData[field.name]} onChange={handleInputChange} placeholder={field.placeholder} className={commonClasses} />;
    };

    return (
        <div className="min-h-screen bg-black text-white p-6 md:p-12 font-sans flex items-center justify-center">
            <div className="max-w-4xl w-full">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-3xl font-bold bg-gradient-to-r from-white to-gray-500 bg-clip-text text-transparent">

                    </h1>
                    <div className="flex items-center gap-4 mt-4">
                        <div className="flex-1 h-2 bg-zinc-800 rounded-full overflow-hidden">
                            <div
                                className="h-full bg-gradient-to-r from-blue-500 to-purple-600 transition-all duration-500 ease-out"
                                style={{ width: `${(currentStep / totalSteps) * 100}%` }}
                            />
                        </div>
                        <span className="text-sm text-gray-400 font-mono">Step {currentStep}/{totalSteps}</span>
                    </div>
                </div>

                {/* Main Card */}
                <div className="bg-zinc-900/50 border border-zinc-800 rounded-3xl p-8 md:p-10 shadow-2xl backdrop-blur-xl">
                    <div className="mb-8">
                        <h2 className="text-2xl font-bold text-white mb-2">{currentQ.title}</h2>
                        <p className="text-gray-400">{currentQ.subtitle}</p>
                    </div>

                    <div className="space-y-6">
                        {currentQ.fields.map(field => (
                            <div key={field.name} className="animate-fade-in-up">
                                <label className="block text-sm font-medium text-gray-300 mb-2 ml-1">
                                    {field.label} {field.required && <span className="text-purple-400">*</span>}
                                </label>
                                {renderField(field)}
                            </div>
                        ))}
                    </div>

                    <div className="flex gap-4 mt-12 pt-6 border-t border-zinc-800">
                        {currentStep > 1 && (
                            <button onClick={prevStep} className="px-6 py-3 rounded-xl font-bold text-gray-400 hover:text-white hover:bg-zinc-800 transition">
                                ← Back
                            </button>
                        )}
                        <button
                            onClick={nextStep}
                            disabled={isSubmitting}
                            className="flex-1 bg-white text-black px-6 py-3 rounded-xl font-bold hover:bg-gray-200 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                        >
                            {isSubmitting ? (
                                <>
                                    <span className="animate-spin text-xl">⟳</span> Processing...
                                </>
                            ) : (
                                currentStep === totalSteps ? 'Submit Application' : 'Continue'
                            )}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LeadQualificationForm;
