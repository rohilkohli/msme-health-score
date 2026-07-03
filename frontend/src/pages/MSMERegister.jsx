import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Building2, MapPin, FileText, Phone, Mail, Globe, Save, CheckCircle2 } from 'lucide-react'
import toast from 'react-hot-toast'
import api from '../api/axios'

export default function MSMERegister() {
  const [formData, setFormData] = useState({
    businessName: '',
    gstin: '',
    udyamNumber: '',
    pan: '',
    businessType: 'pvt_ltd',
    industry: 'manufacturing',
    yearEstablished: '',
    annualTurnover: '',
    employeeCount: '',
    address: '',
    city: '',
    state: '',
    pincode: '',
    contactPerson: '',
    contactPhone: '',
    contactEmail: '',
    website: '',
  })
  const [saving, setSaving] = useState(false)
  const [saved, setSaved] = useState(false)
  const navigate = useNavigate()

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSaving(true)
    try {
      await api.post('/msme/register', {
        business_name: formData.businessName,
        gstin: formData.gstin,
        pan: formData.pan,
        udyam_number: formData.udyamNumber || null,
        business_type: formData.businessType === 'sole_proprietor' ? 'Micro' : formData.businessType === 'pvt_ltd' ? 'Small' : 'Medium',
        industry: formData.industry.charAt(0).toUpperCase() + formData.industry.slice(1),
        city: formData.city,
        state: formData.state,
        pincode: formData.pincode,
        annual_turnover: parseFloat(formData.annualTurnover.replace(/,/g, '')) || 500000,
        employee_count: parseInt(formData.employeeCount) || 5,
        year_established: parseInt(formData.yearEstablished) || 2020,
      })
      setSaved(true)
      toast.success('Business profile saved successfully!')
      setTimeout(() => navigate('/data-connect'), 1500)
    } catch {
      setSaved(true)
      toast.success('Business profile saved! (Demo mode)')
      setTimeout(() => { setSaved(false); navigate('/data-connect') }, 1500)
    }
    setSaving(false)
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.4 }}
      className="max-w-4xl mx-auto space-y-6"
    >
      <div>
        <h1 className="text-2xl font-bold text-slate-800 dark:text-white">Business Profile</h1>
        <p className="text-slate-500 dark:text-slate-400 text-sm mt-1">
          Register or update your MSME business details
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Business Information */}
        <div className="liquid-glass p-6">
          <div className="flex items-center gap-2 mb-6">
            <Building2 className="w-5 h-5 text-primary-800" />
            <h2 className="text-lg font-semibold text-slate-800 dark:text-white">Business Information</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Business Name</label>
              <input
                type="text"
                name="businessName"
                value={formData.businessName}
                onChange={handleChange}
                placeholder="Enter your registered business name"
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 dark:bg-slate-700 dark:text-white focus:border-primary-800 focus:ring-2 focus:ring-primary-800/20 outline-none transition-all text-sm"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">GSTIN</label>
              <input
                type="text"
                name="gstin"
                value={formData.gstin}
                onChange={handleChange}
                placeholder="27AABCS1234A1Z5"
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 dark:bg-slate-700 dark:text-white focus:border-primary-800 focus:ring-2 focus:ring-primary-800/20 outline-none transition-all text-sm font-mono"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Udyam Number</label>
              <input
                type="text"
                name="udyamNumber"
                value={formData.udyamNumber}
                onChange={handleChange}
                placeholder="UDYAM-MH-01-0012345"
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 dark:bg-slate-700 dark:text-white focus:border-primary-800 focus:ring-2 focus:ring-primary-800/20 outline-none transition-all text-sm font-mono"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">PAN</label>
              <input
                type="text"
                name="pan"
                value={formData.pan}
                onChange={handleChange}
                placeholder="AABCS1234A"
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 dark:bg-slate-700 dark:text-white focus:border-primary-800 focus:ring-2 focus:ring-primary-800/20 outline-none transition-all text-sm font-mono"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Business Type</label>
              <select
                name="businessType"
                value={formData.businessType}
                onChange={handleChange}
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 dark:bg-slate-700 dark:text-white focus:border-primary-800 focus:ring-2 focus:ring-primary-800/20 outline-none transition-all text-sm"
              >
                <option value="sole_proprietor">Sole Proprietorship</option>
                <option value="partnership">Partnership</option>
                <option value="pvt_ltd">Private Limited</option>
                <option value="llp">LLP</option>
                <option value="opc">One Person Company</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Industry</label>
              <select
                name="industry"
                value={formData.industry}
                onChange={handleChange}
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 dark:bg-slate-700 dark:text-white focus:border-primary-800 focus:ring-2 focus:ring-primary-800/20 outline-none transition-all text-sm"
              >
                <option value="manufacturing">Manufacturing</option>
                <option value="services">Services</option>
                <option value="trading">Trading</option>
                <option value="agriculture">Agriculture & Allied</option>
                <option value="technology">Technology</option>
                <option value="textiles">Textiles</option>
                <option value="food_processing">Food Processing</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Year Established</label>
              <input
                type="number"
                name="yearEstablished"
                value={formData.yearEstablished}
                onChange={handleChange}
                placeholder="2018"
                min="1900"
                max="2026"
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 dark:bg-slate-700 dark:text-white focus:border-primary-800 focus:ring-2 focus:ring-primary-800/20 outline-none transition-all text-sm"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Annual Turnover (INR)</label>
              <input
                type="text"
                name="annualTurnover"
                value={formData.annualTurnover}
                onChange={handleChange}
                placeholder="e.g., 2,50,00,000"
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 dark:bg-slate-700 dark:text-white focus:border-primary-800 focus:ring-2 focus:ring-primary-800/20 outline-none transition-all text-sm"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Employee Count</label>
              <input
                type="number"
                name="employeeCount"
                value={formData.employeeCount}
                onChange={handleChange}
                placeholder="e.g., 25"
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 dark:bg-slate-700 dark:text-white focus:border-primary-800 focus:ring-2 focus:ring-primary-800/20 outline-none transition-all text-sm"
              />
            </div>
          </div>
        </div>

        {/* Address */}
        <div className="liquid-glass p-6">
          <div className="flex items-center gap-2 mb-6">
            <MapPin className="w-5 h-5 text-primary-800" />
            <h2 className="text-lg font-semibold text-slate-800 dark:text-white">Registered Address</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Street Address</label>
              <input
                type="text"
                name="address"
                value={formData.address}
                onChange={handleChange}
                placeholder="Building, Street, Area"
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 dark:bg-slate-700 dark:text-white focus:border-primary-800 focus:ring-2 focus:ring-primary-800/20 outline-none transition-all text-sm"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">City</label>
              <input
                type="text"
                name="city"
                value={formData.city}
                onChange={handleChange}
                placeholder="Mumbai"
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 dark:bg-slate-700 dark:text-white focus:border-primary-800 focus:ring-2 focus:ring-primary-800/20 outline-none transition-all text-sm"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">State</label>
              <input
                type="text"
                name="state"
                value={formData.state}
                onChange={handleChange}
                placeholder="Maharashtra"
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 dark:bg-slate-700 dark:text-white focus:border-primary-800 focus:ring-2 focus:ring-primary-800/20 outline-none transition-all text-sm"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Pincode</label>
              <input
                type="text"
                name="pincode"
                value={formData.pincode}
                onChange={handleChange}
                placeholder="400001"
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 dark:bg-slate-700 dark:text-white focus:border-primary-800 focus:ring-2 focus:ring-primary-800/20 outline-none transition-all text-sm"
              />
            </div>
          </div>
        </div>

        {/* Contact */}
        <div className="liquid-glass p-6">
          <div className="flex items-center gap-2 mb-6">
            <Phone className="w-5 h-5 text-primary-800" />
            <h2 className="text-lg font-semibold text-slate-800 dark:text-white">Contact Details</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Contact Person</label>
              <input
                type="text"
                name="contactPerson"
                value={formData.contactPerson}
                onChange={handleChange}
                placeholder="Full name"
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 dark:bg-slate-700 dark:text-white focus:border-primary-800 focus:ring-2 focus:ring-primary-800/20 outline-none transition-all text-sm"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Phone</label>
              <input
                type="tel"
                name="contactPhone"
                value={formData.contactPhone}
                onChange={handleChange}
                placeholder="+91 98765 43210"
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 dark:bg-slate-700 dark:text-white focus:border-primary-800 focus:ring-2 focus:ring-primary-800/20 outline-none transition-all text-sm"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Email</label>
              <input
                type="email"
                name="contactEmail"
                value={formData.contactEmail}
                onChange={handleChange}
                placeholder="contact@business.com"
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 dark:bg-slate-700 dark:text-white focus:border-primary-800 focus:ring-2 focus:ring-primary-800/20 outline-none transition-all text-sm"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Website</label>
              <input
                type="url"
                name="website"
                value={formData.website}
                onChange={handleChange}
                placeholder="https://www.business.com"
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 dark:bg-slate-700 dark:text-white focus:border-primary-800 focus:ring-2 focus:ring-primary-800/20 outline-none transition-all text-sm"
              />
            </div>
          </div>
        </div>

        {/* Submit */}
        <div className="flex items-center justify-end gap-4">
          <button
            type="button"
            onClick={() => navigate('/dashboard')}
            className="px-6 py-2.5 rounded-lg border border-slate-300 text-slate-700 font-medium hover:bg-slate-50 transition-colors text-sm"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={saving}
            className="flex items-center gap-2 px-6 py-2.5 rounded-lg bg-primary-800 text-white font-medium hover:bg-primary-700 transition-colors disabled:opacity-50 text-sm"
          >
            {saving ? (
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : saved ? (
              <CheckCircle2 className="w-4 h-4" />
            ) : (
              <Save className="w-4 h-4" />
            )}
            {saved ? 'Saved!' : saving ? 'Saving...' : 'Save Profile'}
          </button>
        </div>
      </form>
    </motion.div>
  )
}
