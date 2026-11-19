import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset directly from GitHub
url = "https://raw.githubusercontent.com/sameekshapoojary26/web-traffic-analytics/main/web_traffic_analytics_v2%20%281%29.csv"

df = pd.read_csv(url)

# Clean dataset
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

for col in ['SessionDurationSec', 'PageViews']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Convert boolean columns
for col in ['Bounced', 'Registered', 'StartedRegistration']:
    df[col] = df[col].astype(str).str.lower().map({
        'true': 1, 'false': 0,
        '1': 1, '0': 0,
        'yes': 1, 'no': 0
    })

df.dropna(subset=['SessionDurationSec', 'PageViews'], inplace=True)

# Basic metrics
total_sessions = len(df)
bounce_rate = df['Bounced'].mean() * 100
avg_duration = df['SessionDurationSec'].mean()
avg_pageviews = df['PageViews'].mean()
conversion_rate = df['Registered'].mean() * 100

print("WEB TRAFFIC ANALYTICS REPORT")
print("============================")
print("Total Sessions:", total_sessions)
print("Bounce Rate:", round(bounce_rate, 2), "%")
print("Average Session Duration:", round(avg_duration, 2), "seconds")
print("Average Pageviews:", round(avg_pageviews, 2))
print("Registration Conversion Rate:", round(conversion_rate, 2), "%")

# Traffic source analysis
print("\nCONVERSION BY TRAFFIC SOURCE")
source_analysis = df.groupby('Source').agg(
    Sessions=('SessionID', 'count'),
    Registrations=('Registered', 'sum')
)
source_analysis['Conversion Rate (%)'] = (
    source_analysis['Registrations'] /
    source_analysis['Sessions'] * 100
)
print(source_analysis)

# Monthly session cohorts (based on session date)
df['Cohort'] = df['Date'].dt.to_period('M').astype(str)

cohort_analysis = df.groupby('Cohort').agg(
    Sessions=('SessionID', 'count'),
    Average_Pageviews=('PageViews', 'mean'),
    Average_Duration=('SessionDurationSec', 'mean')
)

print("\nMONTHLY COHORT ANALYSIS")
print(cohort_analysis)

# Landing page drop-off proxy
landing_analysis = df.groupby('LandingPage').agg(
    Sessions=('SessionID', 'count'),
    Registrations=('Registered', 'sum'),
    Bounces=('Bounced', 'sum')
)

landing_analysis['Conversion Rate (%)'] = (
    landing_analysis['Registrations'] /
    landing_analysis['Sessions'] * 100
)

landing_analysis['Bounce Rate (%)'] = (
    landing_analysis['Bounces'] /
    landing_analysis['Sessions'] * 100
)

print("\nLANDING PAGE PERFORMANCE")
print(landing_analysis.sort_values('Conversion Rate (%)'))

# Chart 1: Traffic sources
plt.figure(figsize=(8,5))
sns.countplot(data=df, x='Source')
plt.title('Website Traffic by Source')
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig('traffic_sources.png')
plt.show()

# Chart 2: Bounce rate by source
bounce_source = df.groupby('Source')['Bounced'].mean() * 100

bounce_source.plot(kind='bar', figsize=(8,5))
plt.title('Bounce Rate by Traffic Source')
plt.ylabel('Bounce Rate (%)')
plt.tight_layout()
plt.savefig('bounce_rate.png')
plt.show()

# Chart 3: Session duration
plt.figure(figsize=(8,5))
sns.boxplot(data=df, x='DeviceCategory',
            y='SessionDurationSec')
plt.title('Session Duration by Device')
plt.tight_layout()
plt.savefig('session_duration.png')
plt.show()

# Chart 4: Conversion by source
source_analysis['Conversion Rate (%)'].plot(
    kind='bar', figsize=(8,5)
)
plt.title('Registration Conversion by Source')
plt.ylabel('Conversion Rate (%)')
plt.tight_layout()
plt.savefig('conversion_rate.png')
plt.show()

# Chart 5: Landing page performance
landing_analysis['Conversion Rate (%)'].sort_values().plot(
    kind='bar', figsize=(9,5)
)
plt.title('Landing Page Conversion Rate')
plt.ylabel('Conversion Rate (%)')
plt.tight_layout()
plt.savefig('landing_page_conversion.png')
plt.show()

# Business recommendations
print("\nBUSINESS RECOMMENDATIONS")
print("========================")
print("1. Improve landing pages with high bounce rates.")
print("2. Invest more in traffic sources with better conversion.")
print("3. Improve website loading speed and user experience.")
print("4. Simplify the registration process.")
print("5. Optimize website experience for different devices.")

# Save results
df.to_csv('web_traffic_analysis_results.csv', index=False)

print("\nWEB TRAFFIC ANALYSIS COMPLETED SUCCESSFULLY!")
