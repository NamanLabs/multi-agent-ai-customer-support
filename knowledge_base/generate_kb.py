"""
Generates the TechMart Electronics knowledge base as PDFs.
Run: python generate_kb.py
"""
from fpdf import FPDF
import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

DOCS = {
    "FAQ.pdf": {
        "title": "TechMart Electronics - Frequently Asked Questions",
        "sections": [
            ("What is TechMart Electronics?",
             "TechMart Electronics is an online and retail electronics company founded in 2018, "
             "specializing in smartphones, laptops, smart home devices, and accessories. We operate "
             "in India with headquarters in Bengaluru and serve customers across 500+ pin codes."),
            ("What are your business hours?",
             "Our customer support is available Monday to Saturday, 9:00 AM to 9:00 PM IST. "
             "Live chat support is available 24/7 through this assistant."),
            ("How do I contact customer support?",
             "You can reach us via this chat assistant, email at support@techmart.example, "
             "or call our helpline at 1800-123-4567 (toll free)."),
            ("Do you have physical stores?",
             "Yes, TechMart has 42 retail stores across major Indian cities including Delhi, "
             "Mumbai, Bengaluru, Hyderabad, Pune, and Chennai."),
            ("Is my personal data safe with TechMart?",
             "Yes. TechMart follows industry-standard encryption for all customer data and does "
             "not share personal information with third parties without consent, in line with "
             "the IT Act, 2000 and applicable data protection regulations."),
            ("Do you offer EMI options?",
             "Yes, TechMart offers no-cost EMI on purchases above Rs. 5,000 through partnered "
             "banks including HDFC, ICICI, and Axis Bank, for tenures of 3, 6, 9, and 12 months."),
        ]
    },
    "RefundPolicy.pdf": {
        "title": "TechMart Electronics - Refund Policy",
        "sections": [
            ("Refund Eligibility",
             "Products purchased from TechMart are eligible for a full refund if returned within "
             "7 days of delivery, provided the item is unused, in original packaging, and all "
             "accessories and manuals are included."),
            ("Non-Refundable Items",
             "Software licenses, gift cards, and items marked 'Final Sale' are not eligible for "
             "refund. Products damaged due to misuse are also excluded."),
            ("Refund Timeline",
             "Once a returned product passes quality inspection, refunds are processed within "
             "5-7 business days. The amount is credited to the original payment method. For "
             "Cash on Delivery orders, refunds are issued via bank transfer within 10 business days."),
            ("Partial Refunds",
             "If a product is returned without original packaging or with missing accessories, "
             "a partial refund of up to 70% of the product value may be issued at TechMart's discretion."),
            ("How to Request a Refund",
             "Refunds can be requested through the 'My Orders' section of the TechMart app or "
             "website, or by contacting customer support with your order ID."),
        ]
    },
    "ShippingPolicy.pdf": {
        "title": "TechMart Electronics - Shipping Policy",
        "sections": [
            ("Delivery Timelines",
             "Standard delivery takes 3-5 business days for metro cities and 5-8 business days "
             "for non-metro locations. Express delivery (1-2 days) is available in select cities "
             "for an additional fee."),
            ("Shipping Charges",
             "Orders above Rs. 999 qualify for free standard shipping. Orders below this threshold "
             "incur a flat shipping fee of Rs. 79."),
            ("Order Tracking",
             "Once shipped, customers receive a tracking link via SMS and email. Orders can also "
             "be tracked in real time through the 'My Orders' section."),
            ("Delayed or Lost Shipments",
             "If a shipment is delayed beyond the estimated delivery window by more than 3 days, "
             "customers are eligible for a shipping fee waiver or store credit of Rs. 100. Lost "
             "shipments are fully refunded or replaced at no cost."),
            ("International Shipping",
             "Currently TechMart ships only within India. International shipping is not supported."),
        ]
    },
    "Warranty.pdf": {
        "title": "TechMart Electronics - Warranty Policy",
        "sections": [
            ("Standard Warranty",
             "All TechMart products come with a standard 1-year manufacturer warranty covering "
             "defects in materials and workmanship, starting from the date of delivery."),
            ("Extended Warranty",
             "Customers can purchase TechMart Care+ at checkout for an additional 1 or 2 years "
             "of coverage, including accidental damage protection for smartphones and laptops."),
            ("What Is Not Covered",
             "Warranty does not cover damage from liquid exposure (unless Care+ is purchased), "
             "unauthorized repairs, physical damage from drops, or normal wear and tear."),
            ("How to Claim Warranty",
             "Warranty claims can be raised through the app under 'My Orders > Request Service', "
             "or by visiting any TechMart service center with proof of purchase."),
            ("Service Center Turnaround",
             "Standard repairs are completed within 7-10 business days. Customers are provided "
             "a loaner device for laptop repairs where available."),
        ]
    },
    "Pricing.pdf": {
        "title": "TechMart Electronics - Pricing Information",
        "sections": [
            ("Pricing Transparency",
             "All prices displayed on the TechMart website and app are inclusive of GST. Prices "
             "may vary slightly between online and retail store listings due to regional taxes."),
            ("Price Match Policy",
             "TechMart offers a price match guarantee: if a customer finds an identical product "
             "at a lower price from an authorized retailer within 7 days of purchase, TechMart "
             "will refund the difference."),
            ("Seasonal Discounts",
             "TechMart runs major sales during Republic Day, Independence Day, and the Diwali "
             "Mega Sale, with discounts up to 40% on select categories."),
            ("Subscription Plans",
             "TechMart Plus membership (Rs. 499/year) offers free express shipping, early access "
             "to sales, and extended return windows of 15 days instead of 7."),
        ]
    },
    "Products.pdf": {
        "title": "TechMart Electronics - Product Catalog Overview",
        "sections": [
            ("Smartphones",
             "TechMart stocks smartphones across budget (under Rs. 15,000), mid-range "
             "(Rs. 15,000-40,000), and premium (above Rs. 40,000) segments from major brands."),
            ("Laptops",
             "Our laptop range includes ultrabooks, gaming laptops, and business laptops, with "
             "configurations ranging from 8GB to 32GB RAM and SSD storage starting at 256GB."),
            ("Smart Home Devices",
             "TechMart offers smart speakers, smart plugs, security cameras, and smart lighting "
             "compatible with both Google Home and Amazon Alexa ecosystems."),
            ("Accessories",
             "We stock chargers, cables, cases, headphones, and power banks, with all electronics "
             "accessories carrying a minimum 6-month warranty."),
            ("Availability",
             "Product availability can be checked in real time on the product page by entering "
             "your delivery pin code."),
        ]
    },
    "InstallationGuide.pdf": {
        "title": "TechMart Electronics - Installation & Setup Guide",
        "sections": [
            ("Smartphone Setup",
             "Power on your device, select your language, connect to Wi-Fi, and sign in with your "
             "Google or Apple account. Restore from backup if migrating from an old device."),
            ("Laptop First Boot",
             "On first boot, complete the Windows or macOS setup wizard, connect to a network, "
             "and install pending system updates before installing third-party software."),
            ("Smart Home Device Pairing",
             "Download the TechMart Home app or the relevant manufacturer app, put the device in "
             "pairing mode by holding the reset button for 5 seconds, and follow in-app instructions."),
            ("Common Installation Errors",
             "If a device fails to pair, ensure it is within 2 meters of the router, restart both "
             "the device and router, and confirm the Wi-Fi is on the 2.4GHz band for older smart devices."),
        ]
    },
    "UserManual.pdf": {
        "title": "TechMart Electronics - General User Manual",
        "sections": [
            ("Account Management",
             "Customers can manage their profile, saved addresses, and payment methods under "
             "'My Account' in the TechMart app or website."),
            ("Order Management",
             "Orders can be viewed, tracked, cancelled (before shipping), or returned under "
             "'My Orders'. Order cancellation after shipping is not permitted; return process "
             "applies instead."),
            ("Password Reset",
             "To reset a forgotten password, click 'Forgot Password' on the login screen and "
             "follow the OTP verification sent to your registered mobile number or email."),
            ("Troubleshooting Login Issues",
             "If OTP is not received, check network signal, wait 60 seconds before requesting "
             "again, and ensure the registered mobile number is correct. Contact support if the "
             "issue persists beyond 3 attempts."),
            ("Loyalty Points",
             "Customers earn 1 TechMart Point for every Rs. 100 spent, redeemable at 1 point = "
             "Rs. 1 on future purchases."),
        ]
    },
}


def build_pdf(filename, title, sections):
    pdf = FPDF()
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)
    pdf.add_page()
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(0, 10, title)
    pdf.set_x(pdf.l_margin)
    pdf.ln(4)
    for heading, body in sections:
        pdf.set_x(pdf.l_margin)
        pdf.set_font("Helvetica", "B", 12)
        pdf.multi_cell(0, 8, heading)
        pdf.set_x(pdf.l_margin)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 6, body)
        pdf.set_x(pdf.l_margin)
        pdf.ln(3)
    pdf.output(os.path.join(OUT_DIR, filename))
    print(f"Created {filename}")


if __name__ == "__main__":
    for fname, content in DOCS.items():
        build_pdf(fname, content["title"], content["sections"])
    print(f"\nDone. {len(DOCS)} knowledge base PDFs created in {OUT_DIR}")
