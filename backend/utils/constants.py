INDIAN_STATES = [
    "Maharashtra", "Karnataka", "Tamil Nadu", "Gujarat", "Rajasthan",
    "Uttar Pradesh", "Delhi", "Telangana", "West Bengal", "Madhya Pradesh",
    "Kerala", "Punjab", "Haryana", "Andhra Pradesh", "Bihar"
]

INDIAN_CITIES = {
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad"],
    "Karnataka": ["Bengaluru", "Mysuru", "Hubli", "Mangaluru", "Belgaum"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Salem", "Tiruchirappalli"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Gandhinagar"],
    "Rajasthan": ["Jaipur", "Udaipur", "Jodhpur", "Kota", "Ajmer"],
    "Uttar Pradesh": ["Lucknow", "Noida", "Kanpur", "Agra", "Varanasi"],
    "Delhi": ["New Delhi", "Dwarka", "Rohini", "Saket", "Karol Bagh"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar", "Khammam"],
    "West Bengal": ["Kolkata", "Howrah", "Durgapur", "Siliguri", "Asansol"],
    "Madhya Pradesh": ["Bhopal", "Indore", "Jabalpur", "Gwalior", "Ujjain"],
    "Kerala": ["Kochi", "Thiruvananthapuram", "Kozhikode", "Thrissur", "Kollam"],
    "Punjab": ["Chandigarh", "Ludhiana", "Amritsar", "Jalandhar", "Patiala"],
    "Haryana": ["Gurugram", "Faridabad", "Panipat", "Ambala", "Karnal"],
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Tirupati", "Nellore"],
    "Bihar": ["Patna", "Gaya", "Muzaffarpur", "Bhagalpur", "Darbhanga"],
}

STATE_CODES = {
    "Maharashtra": "27", "Karnataka": "29", "Tamil Nadu": "33",
    "Gujarat": "24", "Rajasthan": "08", "Uttar Pradesh": "09",
    "Delhi": "07", "Telangana": "36", "West Bengal": "19",
    "Madhya Pradesh": "23", "Kerala": "32", "Punjab": "03",
    "Haryana": "06", "Andhra Pradesh": "37", "Bihar": "10",
}

INDUSTRY_CATEGORIES = [
    "Manufacturing", "Services", "Trading", "Agriculture",
    "Construction", "Technology", "Food Processing", "Textiles",
    "Healthcare", "Logistics"
]

BUSINESS_CATEGORIES = {
    "Manufacturing": [
        "Auto Components", "Plastic Moulding", "Steel Fabrication",
        "Electronics Assembly", "Pharmaceutical", "Chemical Processing"
    ],
    "Services": [
        "IT Services", "Consulting", "Staffing", "Facility Management",
        "Digital Marketing", "Business Process Outsourcing"
    ],
    "Trading": [
        "Wholesale Electronics", "FMCG Distribution", "Building Materials",
        "Industrial Supplies", "Agricultural Commodities", "Textile Trading"
    ],
    "Technology": [
        "Software Development", "Mobile App Development", "Cloud Services",
        "Data Analytics", "Cybersecurity", "IoT Solutions"
    ],
    "Food Processing": [
        "Dairy Products", "Spice Processing", "Bakery", "Packaged Foods",
        "Cold Storage", "Beverage Manufacturing"
    ],
    "Textiles": [
        "Garment Manufacturing", "Fabric Weaving", "Dyeing and Printing",
        "Embroidery", "Home Textiles", "Technical Textiles"
    ],
    "Healthcare": [
        "Diagnostic Lab", "Medical Devices", "Pharmacy Chain",
        "Ayurveda Products", "Hospital Supplies", "Telemedicine"
    ],
    "Logistics": [
        "Freight Forwarding", "Warehousing", "Last Mile Delivery",
        "Cold Chain", "Courier Services", "Fleet Management"
    ],
}

SCORE_WEIGHTS = {
    "revenue_stability": 0.25,
    "cash_flow_health": 0.25,
    "compliance_score": 0.20,
    "growth_trajectory": 0.15,
    "repayment_capacity": 0.15,
}

SCORE_THRESHOLDS = {
    "excellent": 800,
    "good": 600,
    "fair": 400,
    "needs_improvement": 200,
    "critical": 0,
}

LOAN_PRODUCTS = [
    {
        "name": "MSME Working Capital Loan",
        "provider": "IDBI Bank",
        "max_amount": 5000000,
        "interest_rate": "10.5% - 14%",
        "min_score": 600,
        "tenure": "12 months",
    },
    {
        "name": "Mudra Loan - Shishu",
        "provider": "IDBI Bank",
        "max_amount": 50000,
        "interest_rate": "8% - 12%",
        "min_score": 300,
        "tenure": "60 months",
    },
    {
        "name": "Mudra Loan - Kishore",
        "provider": "IDBI Bank",
        "max_amount": 500000,
        "interest_rate": "9% - 13%",
        "min_score": 400,
        "tenure": "60 months",
    },
    {
        "name": "Mudra Loan - Tarun",
        "provider": "IDBI Bank",
        "max_amount": 1000000,
        "interest_rate": "10% - 14%",
        "min_score": 500,
        "tenure": "60 months",
    },
    {
        "name": "MSME Term Loan",
        "provider": "IDBI Bank",
        "max_amount": 10000000,
        "interest_rate": "11% - 15%",
        "min_score": 650,
        "tenure": "84 months",
    },
    {
        "name": "Invoice Discounting (OCEN)",
        "provider": "Multiple NBFCs via OCEN",
        "max_amount": 2000000,
        "interest_rate": "12% - 18%",
        "min_score": 450,
        "tenure": "3 months",
    },
    {
        "name": "Supply Chain Finance",
        "provider": "IDBI Bank + Fintech Partners",
        "max_amount": 3000000,
        "interest_rate": "9% - 13%",
        "min_score": 550,
        "tenure": "6 months",
    },
]

UPI_TRANSACTION_CATEGORIES = [
    "Sales Receipt", "Vendor Payment", "Salary Payment",
    "Utility Payment", "Rent Payment", "Loan EMI",
    "Tax Payment", "Equipment Purchase", "Raw Material",
    "Marketing Expense", "Insurance Premium", "Miscellaneous"
]

BANK_NAMES = [
    "IDBI Bank", "State Bank of India", "HDFC Bank",
    "ICICI Bank", "Axis Bank", "Bank of Baroda",
    "Punjab National Bank", "Canara Bank", "Union Bank of India"
]

IFSC_PREFIXES = {
    "IDBI Bank": "IBKL",
    "State Bank of India": "SBIN",
    "HDFC Bank": "HDFC",
    "ICICI Bank": "ICIC",
    "Axis Bank": "UTIB",
    "Bank of Baroda": "BARB",
    "Punjab National Bank": "PUNB",
    "Canara Bank": "CNRB",
    "Union Bank of India": "UBIN",
}
