"""
GovPilot Database Seeder
Seeds complete, high-fidelity demo environment including the complete hero story:
'AI-Based Public Bus Delay & ETA Improvement' -> Ready for Scale
"""
from datetime import datetime, date, timedelta
from models import (
    db, User, Department, Startup, StartupDeployment, StartupCertification,
    Challenge, EligibilityRequirement, Application, EligibilityScreening,
    Evaluation, EvaluationScore, Pilot, PilotKPI, KPIObservation,
    PilotMilestone, Payment, Risk, Document, ValidationReport, ScaleDecision,
    AuditEvent, Notification
)

def seed_database():
    """Initializes and populates database with realistic demo data."""
    db.create_all()

    # Check if already seeded
    if User.query.filter_by(email='government@govpilot.demo').first():
        return False

    print("[GovPilot Seed] Starting fresh demo data population...")

    # 1. Departments
    dept_transport = Department(
        name="Urban Transport & Mass Transit Authority",
        code="TRANS",
        sector="Urban Mobility & Transport",
        description="Responsible for city bus transit operations, fleet telemetry, route planning, and commuter services.",
        contact_email="transport.innovation@state.gov.in",
        jurisdiction="State Capital Region"
    )
    dept_water = Department(
        name="Municipal Water Supply & Sewerage Board",
        code="WATER",
        sector="Water & Sanitation",
        description="Manages urban potable water distribution pipelines, treatment plants, and non-revenue water reduction.",
        contact_email="water.board@state.gov.in",
        jurisdiction="Greater Metropolitan Area"
    )
    dept_infra = Department(
        name="Public Works & Urban Roads Department",
        code="INFRA",
        sector="Infrastructure & Roads",
        description="Oversees arterial road maintenance, bridge safety inspections, and pavement quality monitoring.",
        contact_email="roads.pwd@state.gov.in",
        jurisdiction="Municipal Corporation"
    )
    dept_waste = Department(
        name="Smart Solid Waste Management Mission",
        code="MSW",
        sector="Municipal Solid Waste & Sanitation",
        description="Supervises door-to-door waste collection, compactor truck routing, and landfill diversion operations.",
        contact_email="sanitation@state.gov.in",
        jurisdiction="Urban Local Body"
    )
    dept_health = Department(
        name="Directorate of Health & Emergency Services",
        code="HEALTH",
        sector="Public Health & Hospitals",
        description="Oversees tertiary district hospitals, emergency room operations, and digital health records.",
        contact_email="health.innovation@state.gov.in",
        jurisdiction="State Health Mission"
    )

    db.session.add_all([dept_transport, dept_water, dept_infra, dept_waste, dept_health])
    db.session.commit()

    # 2. Startups with rich Innovation Passports
    startup_transit = Startup(
        name="TransitAI Labs",
        legal_name="TransitAI Technologies Pvt. Ltd.",
        registration_number="U72900MH2022PTC384912",
        startup_recognition_number="DPIIT-REC-2022-84910",
        founded_year=2022,
        headquarters="Bengaluru, Karnataka",
        website="https://transitai-demo.govpilot.in",
        contact_email="contact@transitai.demo",
        contact_phone="+91 98201 54321",
        founders="Aarav Patel (CTO, ex-ISRO), Neha Sen (CEO, IIM Ahmedabad)",
        employee_count="25-50",
        summary="Deep-tech public transit intelligence company building predictive headway optimization, dynamic ETA forecasting, and edge telemetry models for municipal bus fleets.",
        sector="Urban Mobility & Transport",
        core_technology="Predictive Machine Learning, AIS-140 Telemetry, Edge Computing, Dynamic Route Optimization",
        product_name="PulseTransit Platform v3.4",
        product_description="Enterprise transit intelligence engine connecting with existing vehicle location tracking devices (AIS-140) to synthesize arrival times and prevent bus bunching.",
        architecture_overview="Hybrid Edge-Cloud Architecture. Edge GPS ingestion via MQTT over TLS; ML inference running in secure sovereign cloud; REST/GTFS-RT public endpoints.",
        deployment_model="Hybrid Cloud / Municipal Data Center",
        trl_level="TRL 8 - System Complete and Qualified",
        cybersecurity_certified=True,
        cybersecurity_standard="ISO 27001:2022 & SOC-2 Type II Certified",
        data_residency_compliant=True,
        ip_ownership_clear=True,
        ip_details="100% proprietary source code and registered patent on Dynamic Bus Headway Synchronization (Application #202341029811).",
        liability_insurance=True,
        capabilities="Computer Vision, Telemetry Ingestion, Municipal GIS Integration, GTFS-RT APIs, Route Optimization, Machine Learning"
    )

    startup_urbanflow = Startup(
        name="UrbanFlow Systems",
        legal_name="UrbanFlow Logistics Pvt. Ltd.",
        registration_number="U74999DL2023PTC412345",
        startup_recognition_number="DPIIT-REC-2023-11928",
        founded_year=2023,
        headquarters="New Delhi",
        website="https://urbanflow.demo",
        contact_email="info@urbanflow.demo",
        founders="Kunal Shah, Dr. Meenakshi Sundaram",
        employee_count="15-30",
        summary="IoT sensor networks and smart city traffic signal synchronization algorithms.",
        sector="Urban Mobility & Transport",
        core_technology="IoT Telemetry, Micro-traffic Simulation, Edge Gateways",
        product_name="FlowSync Edge",
        product_description="Traffic corridor optimization via real-time queue sensing.",
        deployment_model="Cloud SaaS",
        trl_level="TRL 7 - Prototype Demonstrated",
        cybersecurity_certified=True,
        cybersecurity_standard="ISO 27001 Certified",
        data_residency_compliant=True,
        ip_ownership_clear=True,
        capabilities="IoT Telemetry, Traffic Signal Priority, Municipal Integration, Cloud Analytics"
    )

    startup_mobilityvision = Startup(
        name="MobilityVision",
        legal_name="MobilityVision Analytics LLP",
        registration_number="AAW-9012",
        startup_recognition_number="DPIIT-REC-2023-44120",
        founded_year=2023,
        headquarters="Pune, Maharashtra",
        website="https://mobilityvision.demo",
        contact_email="sales@mobilityvision.demo",
        founders="Vikram Nair, Shweta Kulkarni",
        employee_count="10-20",
        summary="Edge computer vision cameras for onboard transit passenger counting and crowd density estimation.",
        sector="Urban Mobility & Transport",
        core_technology="Edge AI, Computer Vision, Optical Flow, Privacy Blurring",
        product_name="VisionCrowd AI",
        product_description="Onboard camera system for automatic passenger counting and seat occupancy analytics.",
        deployment_model="Edge Appliance",
        trl_level="TRL 7 - Prototype Demonstrated",
        cybersecurity_certified=True,
        cybersecurity_standard="CERT-In Security Cleared",
        data_residency_compliant=True,
        ip_ownership_clear=True,
        capabilities="Computer Vision, Edge AI, Privacy Redaction, Fleet Telemetry"
    )

    startup_roadvision = Startup(
        name="RoadVision AI",
        legal_name="RoadVision Technologies Inc.",
        registration_number="U72200KA2021PTC145678",
        startup_recognition_number="DPIIT-REC-2021-39281",
        founded_year=2021,
        headquarters="Hyderabad, Telangana",
        website="https://roadvision.demo",
        contact_email="contact@roadvision.demo",
        founders="Siddharth Rao, Ananya Mukherjee",
        employee_count="30-60",
        summary="Vehicle-mounted computer vision camera modules for real-time automated pothole, crack, and pavement distress classification.",
        sector="Infrastructure & Roads",
        core_technology="Computer Vision, 3D Depth Estimation, Municipal GIS, Work-Order Automation",
        product_name="RoadSense Pavement AI",
        product_description="High-speed road surface scanner operating at up to 80 km/h with sub-millimeter fissure detection.",
        deployment_model="Edge AI Device + Cloud Portal",
        trl_level="TRL 8 - System Qualified",
        cybersecurity_certified=True,
        cybersecurity_standard="ISO 27001 & ISO 9001",
        data_residency_compliant=True,
        ip_ownership_clear=True,
        capabilities="Computer Vision, Road Infrastructure, Municipal GIS, Similar Deployment, Pothole Detection"
    )

    startup_aquasense = Startup(
        name="AquaSense Technologies",
        legal_name="AquaSense Water Tech Pvt. Ltd.",
        registration_number="U41000TN2022PTC156789",
        startup_recognition_number="DPIIT-REC-2022-55678",
        founded_year=2022,
        headquarters="Chennai, Tamil Nadu",
        website="https://aquasense.demo",
        contact_email="support@aquasense.demo",
        founders="Dr. Ramesh Balan, Preeti Iyer",
        employee_count="20-40",
        summary="Acoustic hydrophone IoT sensors and AI pressure wave algorithms to isolate subsurface pipeline leaks within 5 meters.",
        sector="Water & Sanitation",
        core_technology="Acoustic IoT, Hydraulic Modeling, Machine Learning, LoRaWAN",
        product_name="HydroLeak Sentinel",
        product_description="Non-invasive water pipe leak detection and non-revenue water mitigation.",
        deployment_model="On-Prem / Cloud",
        trl_level="TRL 8 - Operational",
        cybersecurity_certified=True,
        cybersecurity_standard="ISO 27001",
        data_residency_compliant=True,
        ip_ownership_clear=True,
        capabilities="Acoustic Sensors, IoT Telemetry, Water Infrastructure, SCADA Integration"
    )

    db.session.add_all([startup_transit, startup_urbanflow, startup_mobilityvision, startup_roadvision, startup_aquasense])
    db.session.commit()

    # Add deployments & certifications for TransitAI Labs
    d1 = StartupDeployment(
        startup_id=startup_transit.id,
        client_name="Metropolitan Transport Corporation",
        client_type="Municipal Transit Agency",
        project_title="Route 21 & 45 Headway Synchronization Pilot",
        scale="25 Buses, 30 Days",
        duration="3 Months (2024)",
        outcome_summary="Achieved 28% reduction in passenger wait times and 94% ETA precision across 15,000 daily trips.",
        year=2024
    )
    d2 = StartupDeployment(
        startup_id=startup_transit.id,
        client_name="State Road Transport Department",
        client_type="State Government",
        project_title="Intercity Bus Live ETA Telemetry Integration",
        scale="50 Long-distance Coaches",
        duration="6 Months (2025)",
        outcome_summary="Integrated AIS-140 GPS streams into state traveler app with 99.8% uptime.",
        year=2025
    )
    c1 = StartupCertification(
        startup_id=startup_transit.id,
        name="ISO/IEC 27001:2022 Information Security Management",
        issuing_body="BSI Assurance Group",
        valid_until="2027-12-31",
        verification_url="https://verify.bsigroup.com/IS-784910"
    )
    c2 = StartupCertification(
        startup_id=startup_transit.id,
        name="DPIIT Recognized Startup (Government of India)",
        issuing_body="Department for Promotion of Industry and Internal Trade",
        valid_until="2032-05-15",
        verification_url="https://startupindia.gov.in/verify/DPIIT84910"
    )
    db.session.add_all([d1, d2, c1, c2])

    # Add deployment for RoadVision AI
    rd1 = StartupDeployment(
        startup_id=startup_roadvision.id,
        client_name="City Municipal Corporation PWD",
        client_type="Municipal Corporation",
        project_title="Automated Road Pothole Survey & GIS Mapping",
        scale="120 km Municipal Arterials",
        duration="4 Months (2024)",
        outcome_summary="Identified 1,420 pavement defects with 93.4% precision, cutting repair backlog by 60%.",
        year=2024
    )
    db.session.add(rd1)
    db.session.commit()

    # 3. Demo Users
    user_gov = User(
        email="government@govpilot.demo",
        name="Rajesh Verma",
        role="government",
        title="Chief Innovation & Technology Officer",
        phone="+91 98110 20011",
        department_id=dept_transport.id
    )
    user_gov.set_password("Password123")

    user_startup = User(
        email="startup@innovate.demo",
        name="Aarav Patel",
        role="startup",
        title="Founder & CEO",
        phone="+91 98201 54321",
        startup_id=startup_transit.id
    )
    user_startup.set_password("Password123")

    user_expert = User(
        email="expert@review.demo",
        name="Dr. Sunita Mehra",
        role="evaluator",
        title="Senior Transport Systems Evaluator",
        phone="+91 94440 33221"
    )
    user_expert.set_password("Password123")

    user_validator = User(
        email="validator@audit.demo",
        name="Vikram Deshmukh",
        role="validator",
        title="Lead Auditor, National Technical Audit Cell",
        phone="+91 97110 44556"
    )
    user_validator.set_password("Password123")

    user_admin = User(
        email="admin@govpilot.demo",
        name="Sanjay Kulkarni",
        role="admin",
        title="GovPilot Platform Administrator",
        phone="+91 99990 00001"
    )
    user_admin.set_password("Password123")

    db.session.add_all([user_gov, user_startup, user_expert, user_validator, user_admin])
    db.session.commit()

    # 4. Challenges
    # Hero Challenge: AI-Based Public Bus Delay & ETA Improvement
    hero_challenge = Challenge(
        code="CH-TRANS-2026-001",
        title="AI-Based Public Bus Delay Prediction & Dynamic ETA Improvement",
        department_id=dept_transport.id,
        sector="Urban Mobility & Transport",
        status="pilot_active",
        problem_summary="City buses suffer from unpredictable delays, vehicle bunching, and inaccurate passenger arrival predictions during peak urban traffic hours.",
        problem_details="Fixed timetable scheduling breaks down under variable city traffic conditions. Passengers experience high and unpredictable wait times at bus stops, while depot dispatchers lack real-time predictive insights to regulate bus headways.",
        urgency_level="High",
        baseline_summary="Average passenger wait time at corridor bus stops is 16.4 minutes. Timetable adherence during peak morning and evening rush hours is only 61.2%. Commuter app ETA accuracy (within 90 seconds) is below 58%.",
        current_process="Depot supervisors monitor static vehicle location dots on legacy screens and issue reactive voice instructions over radio only after major gridlocks occur.",
        pain_points="Severe bus bunching (multiple buses arriving simultaneously followed by 30-minute gaps); commuter dissatisfaction; lack of automated headway regulation.",
        affected_users="450,000 Daily Transit Commuters, 380 Bus Operators, 18 Depot Operations Controllers",
        expected_outcome="Deploy an AI-powered telemetry analysis and predictive headway regulation engine that synchronizes transit intervals and delivers accurate real-time arrival forecasts to commuter applications.",
        target_improvement="Reduce average passenger wait times by >30%, improve schedule/headway adherence to >85%, and achieve ETA accuracy >92%.",
        target_kpis_summary="1. Passenger Waiting Time (<11 min)\n2. ETA Accuracy (>92%)\n3. Headway Regularity (>85%)\n4. System Telemetry Uptime (>99.5%)",
        geography="5 Major Urban Transit Corridors (Total 42 Bus Stops)",
        target_users_count="10 Transit Buses, 3 Depot Managers, 25,000 Daily Corridor Passengers",
        test_facilities="Central Transport Control Center (TCC) & City Depot #3 Operations Lab",
        duration_days=90,
        budget_indicative="₹10,00,000",
        available_datasets="Live AIS-140 GPS Telemetry Stream, 12 Months Historical Transit Logs, Automated Fare Collection (AFC) Passenger Counts",
        data_sensitivity="Public Transit Data / Anonymized Commuter Travel Flow Metrics",
        api_availability="Real-time WebSocket & REST GTFS-RT Feeds with 5-second polling",
        technical_constraints="Must interface with existing vehicle GPS transponders without requiring hardware overhaul; latency under 2 seconds for ETA push.",
        security_requirements="Role-based access control; TLS 1.3 encrypted data channels; compliance with National Data Sharing and Accessibility Policy (NDSAP).",
        integration_requirements="Direct bidirectional sync with Municipal Traffic Signal Priority (TSP) feeds and the State Commuter Mobile App API.",
        evaluation_criteria_notes="Technical Feasibility (25%), Expected Outcome & Delay Reduction (25%), Scalability to 500+ Buses (15%), Security & Data Privacy (15%), Implementation Readiness (10%), Cost-to-Value (10%)",
        success_thresholds="Wait time reduction >= 25%, ETA prediction error <= 90 seconds across 90% of trips, System availability >= 99.5%.",
        created_by_user_id=user_gov.id,
        published_at=datetime.utcnow() - timedelta(days=95),
        application_deadline=datetime.utcnow() - timedelta(days=70)
    )

    # Additional Realistic Challenges
    c2 = Challenge(
        code="CH-WATER-2026-002",
        title="Subsurface Acoustic & Pressure IoT Analytics for Non-Revenue Water Leak Detection",
        department_id=dept_water.id,
        sector="Water & Sanitation",
        status="published",
        problem_summary="Underground potable water distribution pipelines experience persistent hidden leaks, losing over 34% of treated water before reaching consumer meters.",
        problem_details="Traditional acoustic listening rods are manual and slow. Pinpointing pinhole leaks takes an average of 6.5 days, resulting in immense non-revenue water loss and localized road sinkholes.",
        urgency_level="Critical",
        baseline_summary="Non-Revenue Water loss is 34.2%. Average time to localize an underground pipe leak is 156 hours.",
        current_process="Field technicians conduct manual nighttime acoustic rod inspections across 400 km of buried pipe network.",
        pain_points="Delayed leak discovery; high water loss; street cave-ins; expensive emergency excavations.",
        affected_users="Water Board Engineers, 1.2M Municipal Residents, Maintenance Crews",
        expected_outcome="Deploy acoustic hydrophone IoT sensors and AI pressure wave algorithms to isolate underground leaks within 5 meters within 6 hours.",
        target_improvement="Cut leak detection time by 80% and reduce localized non-revenue water loss by 18%.",
        target_kpis_summary="Leak Localization Accuracy (<5m), Mean Time to Detect (<6h), Water Loss Reduction (>15%)",
        geography="District Metered Area 7 (14 km Secondary Pipeline Network)",
        target_users_count="6 Hydraulic Engineers & 18 Zone Maintenance Workers",
        test_facilities="Municipal Water Quality & Flow Monitoring Station B",
        duration_days=90,
        budget_indicative="₹12,00,000",
        available_datasets="SCADA Pumping Telemetry, DMA Meter Data, Pipe Network GIS Shapefiles",
        data_sensitivity="Critical Public Infrastructure Data / Restricted Access",
        api_availability="OPC-UA / MQTT SCADA Gateway and GIS Web Feature Services",
        technical_constraints="Submersible sensors (IP68) with LoRaWAN/NB-IoT telemetry operating in underground concrete chambers.",
        security_requirements="End-to-end AES-256 payload encryption; isolated SCADA gateway network segment.",
        integration_requirements="Integration with Water Board SCADA & Automated Valve Actuator Telemetry.",
        evaluation_criteria_notes="Leak precision (30%), Sensor power autonomy (20%), False alarm rejection (20%), Cost efficiency (15%), Integration readiness (15%)",
        success_thresholds="Accurate detection of simulated and organic leaks >90% within 8 hours; zero false positive major excavation orders.",
        created_by_user_id=user_gov.id,
        published_at=datetime.utcnow() - timedelta(days=20),
        application_deadline=datetime.utcnow() + timedelta(days=25)
    )

    c3 = Challenge(
        code="CH-INFRA-2026-003",
        title="AI Pavement Distress Detection & Automated Municipal Work-Order Generation",
        department_id=dept_infra.id,
        sector="Infrastructure & Roads",
        status="published",
        problem_summary="Manual road inspection is resource-intensive, slow, and reactive, leading to hazardous potholes remaining undetected for weeks.",
        problem_details="Municipal inspection teams drive survey vans with clipboards. Inspection cycles take 3 weeks per zone, leading to severe pavement degradation during monsoon seasons.",
        urgency_level="High",
        baseline_summary="Manual survey coverage is 15 km/day with a 72-hour delay between defect emergence and municipal notification. Detection accuracy of minor fissures is below 60%.",
        current_process="Field inspectors drive at 20 km/h manually photographing defects on tablets and uploading reports at day end.",
        pain_points="High labor cost; 3 to 5-day latency in work order dispatch; inability to survey at night or adverse weather.",
        affected_users="Road Maintenance Engineers, City Commuters, Emergency Fleets",
        expected_outcome="Vehicle-mounted computer vision camera modules to autonomously classify, measure (depth/area), and geo-tag pavement distress in real-time, feeding automated work orders into municipal ERP.",
        target_improvement="Reduce defect discovery-to-work-order time by 85%, improve detection precision to >92%, and double daily route coverage.",
        target_kpis_summary="Pothole Detection Precision (>90%), Inspection Speed (60 km/day), Mean Time to Notice (<4 hours)",
        geography="5 Central Municipal Corridors (80 lane-km total)",
        target_users_count="12 Field Road Maintenance Officers & 4 Central Dispatchers",
        test_facilities="Central Municipal Fleet Depot & Smart City GIS Command Room",
        duration_days=60,
        budget_indicative="₹8,50,000",
        available_datasets="High-resolution City GIS Base Map, 3-Year Historical Road Repair Logs, Municipal Fleet Telemetry Stream",
        data_sensitivity="Confidential / Municipal Internal Infrastructure Layer",
        api_availability="REST APIs with OAuth2 Sandbox Access & GeoJSON streaming endpoints",
        technical_constraints="Edge inference must operate on vehicle 12V power without sustained 4G connectivity; IP67 weather-proofing required.",
        security_requirements="All video frames must be anonymized (blurring citizen faces and civilian vehicle license plates at edge before transmission).",
        integration_requirements="Direct bi-directional sync with Municipal GIS & Public Works Work-Order Management System.",
        evaluation_criteria_notes="Technical precision of 3D depth estimation (25%), Edge compute reliability (25%), Fleet compatibility (15%), Security & privacy redaction (15%), Pan-city scale readiness (20%)",
        success_thresholds="Average detection precision >= 90%, Zero privacy redaction breaches, Minimum 98% edge node uptime during pilot period.",
        created_by_user_id=user_gov.id,
        published_at=datetime.utcnow() - timedelta(days=15),
        application_deadline=datetime.utcnow() + timedelta(days=30)
    )

    c4 = Challenge(
        code="CH-MSW-2026-004",
        title="IoT Fill-Level Sensors & Dynamic Route Optimization for Municipal Waste Fleets",
        department_id=dept_waste.id,
        sector="Municipal Solid Waste & Sanitation",
        status="published",
        problem_summary="Fixed garbage collection routes lead to overflowing community bins and wasteful fuel consumption.",
        problem_details="Collection trucks follow static daily schedules regardless of whether bins are 20% or 110% full, causing visual blight, odor complaints, and excessive diesel expenditure.",
        urgency_level="Medium",
        baseline_summary="Bin overflow incident rate is 24.8%. Average fuel expenditure per metric ton of collected waste is ₹1,420.",
        current_process="Fixed circular truck routes every morning covering 120 designated community dumpsters.",
        pain_points="Frequent citizen complaints regarding overflowing bins; high diesel fuel consumption; inability to dynamically re-route.",
        affected_users="Sanitation Supervisors, 8 Truck Drivers, 65,000 Ward Residents",
        expected_outcome="Equip municipal bins with ruggedized optical/ultrasonic fill sensors and generate dynamic daily optimal collection routes for fleet dispatch.",
        target_improvement="Eliminate bin overflows by >85% while cutting collection fleet fuel mileage by 22%.",
        target_kpis_summary="Bin Overflow Rate (<3%), Fleet Fuel Savings (>20%), Route Completion Time (<4.5 hrs)",
        geography="Municipal Ward 14 & Ward 15 (85 Community Bins, 8 Compactor Trucks)",
        target_users_count="8 Truck Drivers, 2 Sanitation Supervisors",
        test_facilities="Ward 14 Sanitation Depot & Solid Waste Control Dashboard",
        duration_days=60,
        budget_indicative="₹7,50,000",
        available_datasets="Daily Waste Weight Weighbridge Records, Bin Geo-locations, Municipal Truck Fleet GPS Traces",
        data_sensitivity="Internal Municipal Logistics Data",
        api_availability="Fleet GPS REST API & Sanitation GIS layer",
        technical_constraints="Sensors must withstand corrosive environment, steam washing, and 45°C ambient temperatures.",
        security_requirements="TLS encrypted sensor data; authenticated driver tablet applications.",
        integration_requirements="Sync with Municipal Weighbridge ERP and Citizen Grievance Portal.",
        evaluation_criteria_notes="Sensor ruggedness (25%), Dynamic route optimization efficiency (25%), Driver UI ease of use (20%), Solution TCO (15%), Security (15%)",
        success_thresholds="Reduction of bin overflow incidents to <3%; demonstrable 18%+ reduction in fleet diesel consumption.",
        created_by_user_id=user_gov.id,
        published_at=datetime.utcnow() - timedelta(days=10),
        application_deadline=datetime.utcnow() + timedelta(days=35)
    )

    c5 = Challenge(
        code="CH-HEALTH-2026-005",
        title="AI-Powered Emergency Department Clinical Triage & Queue Streamlining",
        department_id=dept_health.id,
        sector="Public Health & Hospitals",
        status="in_evaluation",
        problem_summary="District hospital emergency rooms face acute overcrowding and triage acuity delays.",
        problem_details="Clinical staff face severe cognitive overload during peak intake hours, leading to prolonged patient waiting times and delayed prioritization of deteriorating patients.",
        urgency_level="Critical",
        baseline_summary="Average triage wait time for Category 3/4 patients is 48 minutes. Triage protocol discordance rate is 14.5%.",
        current_process="Paper-based Emergency Severity Index (ESI) scoring recorded by triage nurses followed by manual physical token dispatch.",
        pain_points="High wait times; risk of unrecognized clinical deterioration in waiting areas; excessive documentation burden.",
        affected_users="14 Triage Nurses, 6 Emergency Medical Officers, 220 Daily Patients",
        expected_outcome="Implement an AI-assisted clinical decision support triage interface combining contactless vital sign telemetry with conversational symptom assessment to accelerate safe triage assignment.",
        target_improvement="Reduce triage intake time by 55% while reducing acuity misclassification by >60%.",
        target_kpis_summary="Door-to-Triage Time (<15 min), ESI Agreement Rate (>95%), Nursing Documentation Time (<3 min)",
        geography="District General Hospital Emergency Department (35 Bed Capacity)",
        target_users_count="14 Triage Nurses, 6 Emergency Medical Officers, 220 Daily Patients",
        test_facilities="District General Hospital ER Triage Bay 1 & 2",
        duration_days=90,
        budget_indicative="₹14,00,000",
        available_datasets="Anonymized Historical ER Admission EHR Records, Vital Sign Waveforms",
        data_sensitivity="Protected Health Information (PHI) / DISHA / HIPAA Equivalent High Sensitivity",
        api_availability="HL7 FHIR v4.0 API Endpoints & DICOM Connectors",
        technical_constraints="On-premise edge appliance execution with zero external public cloud PHI transfer; 99.99% high availability.",
        security_requirements="Strict role-based access, full audit logging of every AI inference recommendation, data-at-rest encryption.",
        integration_requirements="Direct bidirectional integration with Hospital Information Management System (HIMS) and Vital Monitors.",
        evaluation_criteria_notes="Clinical validation & safety margins (35%), Data privacy & on-prem compliance (25%), Nurse UX (20%), FHIR integration (20%)",
        success_thresholds="Zero safety critical misclassifications, ESI gold-standard concordance >92%, 40%+ reduction in triage desk latency.",
        created_by_user_id=user_gov.id,
        published_at=datetime.utcnow() - timedelta(days=40),
        application_deadline=datetime.utcnow() - timedelta(days=5)
    )

    db.session.add_all([hero_challenge, c2, c3, c4, c5])
    db.session.commit()

    # Add eligibility criteria for hero challenge
    req1 = EligibilityRequirement(challenge_id=hero_challenge.id, criterion_title="DPIIT / State Startup Recognition Certificate", description="Must be an officially registered and recognized startup entity.", requirement_type="Recognition")
    req2 = EligibilityRequirement(challenge_id=hero_challenge.id, criterion_title="AIS-140 Vehicle Telemetry Compatibility", description="Proprietary software must ingest standard NMEA/AIS-140 GPS data streams without specialized vehicle modding.", requirement_type="Technical")
    req3 = EligibilityRequirement(challenge_id=hero_challenge.id, criterion_title="ISO 27001 or SOC-2 Type II Cybersecurity Certification", description="Demonstrated information security practices for handling live transport streams.", requirement_type="Compliance")
    req4 = EligibilityRequirement(challenge_id=hero_challenge.id, criterion_title="Prior Municipal or Fleet Deployment Reference", description="Minimum one pilot or production deployment in public/private transport.", requirement_type="Experience")
    db.session.add_all([req1, req2, req3, req4])
    db.session.commit()

    # 5. Three Startup Applications for the Hero Challenge
    app_transit = Application(
        code="APP-2026-0042",
        challenge_id=hero_challenge.id,
        startup_id=startup_transit.id,
        submitted_by_user_id=user_startup.id,
        status="pilot_selected",
        solution_title="PulseTransit: Edge Telemetry Ingestion & Dynamic Headway Synchronization",
        solution_summary="PulseTransit ingest AIS-140 GPS telemetry in real-time, calculates rolling delay probabilities via neural kalman filters, and provides dynamic holding/speed-adjustment advisories to drivers while streaming sub-90s accurate ETAs to passenger apps.",
        product_readiness_trl="TRL 8 - System Complete and Qualified",
        problem_alignment="Directly tackles bus bunching and inaccurate arrival predictions through dynamic schedule synchronization rather than static timetable tracking.",
        technical_approach="1. Ingest 5-sec GPS bursts via MQTT broker.\n2. Predict segment speeds based on real-time traffic signal cycles & historical delay graphs.\n3. Output dynamic headway regulation advisories to depot screens and driver consoles.\n4. Push GTFS-RT protobuf feed to commuter apps.",
        implementation_plan="Week 1-2: API handshake with Transport Control Center.\nWeek 3-4: Onboard 10 buses across 5 routes.\nWeek 5-8: Model training and driver advisory calibration.\nWeek 9-12: Full live public ETA broadcast and KPI validation.",
        duration_weeks=12,
        resource_requirements="Sandbox access to 10 bus AIS-140 feeds, driver app tablet mounting clips, TCC dashboard display terminal.",
        expected_outcomes="30%+ reduction in passenger wait time variance, 94%+ ETA accuracy, zero server downtime.",
        proposed_kpis="Passenger Wait Time, ETA Accuracy (within 90s), Headway Adherence Index, System Uptime",
        technical_specs="Containerized microservices running Python/Go, PostgreSQL/TimescaleDB, Redis caching, sub-200ms API response latency.",
        data_governance_plan="All passenger queries anonymized. No PII collected. Telemetry encrypted with TLS 1.3.",
        cloud_vs_edge="Hybrid Cloud Edge",
        budget_total="₹10,00,000",
        budget_breakdown="₹3,50,000 Model Training & API Integration\n₹2,50,000 Driver App Deployment & Training\n₹2,00,000 Cloud Compute & Telemetry Ingestion\n₹2,00,000 Project Management & Field Support",
        eligibility_status="verified",
        eligibility_notes="All 4 mandatory requirements verified. Startup recognized by DPIIT, holds ISO 27001 certification, and provided 2 municipal transit references.",
        eligibility_reviewed_by_id=user_gov.id,
        eligibility_reviewed_at=datetime.utcnow() - timedelta(days=65),
        average_score=91.2,
        created_at=datetime.utcnow() - timedelta(days=68)
    )

    app_urbanflow = Application(
        code="APP-2026-0043",
        challenge_id=hero_challenge.id,
        startup_id=startup_urbanflow.id,
        submitted_by_user_id=user_startup.id,
        status="in_evaluation",
        solution_title="FlowSync Transit: IoT Corridor Signal Priority & Delay Reduction",
        solution_summary="FlowSync deploys roadside IoT receivers along bus stops to request green-light extensions for delayed buses at major signalized intersections.",
        product_readiness_trl="TRL 7 - System Prototype Demonstrated",
        problem_alignment="Reduces bus delay by addressing intersection wait times via traffic light coordination.",
        technical_approach="Corridor-based micro-traffic simulation and IoT signal controllers with DSRC/cellular communication.",
        implementation_plan="12-week deployment covering 8 signalized intersections and 10 buses.",
        duration_weeks=12,
        expected_outcomes="18% reduction in corridor travel time, improved intersection throughput.",
        budget_total="₹9,20,000",
        eligibility_status="verified",
        eligibility_notes="Meets recognition and technical criteria. Security documentation verified.",
        eligibility_reviewed_by_id=user_gov.id,
        eligibility_reviewed_at=datetime.utcnow() - timedelta(days=64),
        average_score=87.8,
        created_at=datetime.utcnow() - timedelta(days=67)
    )

    app_mobilityvision = Application(
        code="APP-2026-0044",
        challenge_id=hero_challenge.id,
        startup_id=startup_mobilityvision.id,
        submitted_by_user_id=user_startup.id,
        status="in_evaluation",
        solution_title="VisionCrowd: Passenger Density Sensing & Boarding Delay Analytics",
        solution_summary="VisionCrowd uses edge optical sensors installed above bus doors to calculate boarding/alighting dwell times and broadcast crowding indicators.",
        product_readiness_trl="TRL 7 - System Prototype Demonstrated",
        problem_alignment="Addresses passenger crowding and dwell time delays at busy terminal stops.",
        technical_approach="Onboard edge AI camera calculating optical flow passenger counts with real-time face blurring.",
        implementation_plan="Install edge cameras in 10 test buses over 10 weeks.",
        duration_weeks=10,
        expected_outcomes="Accurate dwell time prediction and passenger crowding level indicators.",
        budget_total="₹8,80,000",
        eligibility_status="verified",
        eligibility_notes="Eligibility verified. Facial privacy blurring compliance reviewed.",
        eligibility_reviewed_by_id=user_gov.id,
        eligibility_reviewed_at=datetime.utcnow() - timedelta(days=64),
        average_score=81.5,
        created_at=datetime.utcnow() - timedelta(days=66)
    )

    db.session.add_all([app_transit, app_urbanflow, app_mobilityvision])
    db.session.commit()

    # Add screening items for TransitAI Labs
    s1 = EligibilityScreening(application_id=app_transit.id, criterion_name="Startup Recognition (DPIIT)", is_passed=True, remarks="Verified #DPIIT-REC-2022-84910")
    s2 = EligibilityScreening(application_id=app_transit.id, criterion_name="AIS-140 GPS Compatibility", is_passed=True, remarks="Standard NMEA & REST ingestion verified")
    s3 = EligibilityScreening(application_id=app_transit.id, criterion_name="Cybersecurity Certification", is_passed=True, remarks="ISO 27001:2022 valid until 2027")
    s4 = EligibilityScreening(application_id=app_transit.id, criterion_name="Prior Deployment Experience", is_passed=True, remarks="2 successful transport pilots documented")
    db.session.add_all([s1, s2, s3, s4])

    # 6. Expert Evaluations
    eval_transit = Evaluation(
        application_id=app_transit.id,
        evaluator_id=user_expert.id,
        technical_feasibility_score=94.0,
        technical_feasibility_comment="Exceptional technical architecture. Pure software/API layer leveraging existing AIS-140 GPS transponders ensures zero hardware disruption.",
        expected_outcome_score=92.0,
        expected_outcome_comment="Strong methodology for dynamic headway synchronization. Simulated data shows consistent 28-32% reduction in bus bunching.",
        scalability_score=90.0,
        scalability_comment="Cloud-native microservices architecture effortlessly scales from 10 buses to the entire city fleet of 450 buses.",
        security_risk_score=88.0,
        security_risk_comment="ISO 27001 certified. Robust data handling policy with encrypted channels and zero passenger PII retention.",
        implementation_readiness_score=92.0,
        implementation_readiness_comment="TRL 8 maturity with plug-and-play APIs ready for immediate sandbox ingestion.",
        cost_value_score=90.0,
        cost_value_comment="Well-budgeted proposal at ₹10 Lakhs. Excellent value-for-money given direct passenger impact.",
        total_weighted_score=91.2,
        conflict_of_interest_cleared=True,
        coi_declaration_text="I confirm that I have no conflict of interest in this evaluation.",
        status="submitted",
        overall_recommendation="Strongly Recommend for Pilot Selection",
        general_remarks="Top-ranked proposal with clear, measurable outcome metrics and proven technical readiness for city bus operations.",
        created_at=datetime.utcnow() - timedelta(days=60),
        submitted_at=datetime.utcnow() - timedelta(days=58)
    )

    eval_urbanflow = Evaluation(
        application_id=app_urbanflow.id,
        evaluator_id=user_expert.id,
        technical_feasibility_score=86.0,
        technical_feasibility_comment="Good signal priority concept, but requires coordination with traffic police controllers.",
        expected_outcome_score=88.0,
        expected_outcome_comment="Directly improves corridor speeds, but less impact on headway synchronization.",
        scalability_score=91.0,
        scalability_comment="Corridor-by-corridor scalability is straightforward.",
        security_risk_score=86.0,
        security_risk_comment="Standard IoT security measures in place.",
        implementation_readiness_score=85.0,
        implementation_readiness_comment="Requires field calibration at traffic light intersections.",
        cost_value_score=88.0,
        cost_value_comment="Reasonable hardware and installation budget.",
        total_weighted_score=87.8,
        conflict_of_interest_cleared=True,
        status="submitted",
        overall_recommendation="Recommend with Standard Oversight",
        general_remarks="Viable proposal, but slightly more complex physical deployment requirements than TransitAI.",
        created_at=datetime.utcnow() - timedelta(days=60),
        submitted_at=datetime.utcnow() - timedelta(days=58)
    )

    eval_mobilityvision = Evaluation(
        application_id=app_mobilityvision.id,
        evaluator_id=user_expert.id,
        technical_feasibility_score=82.0,
        technical_feasibility_comment="Computer vision for passenger counting is well-designed, but optical cameras require regular physical lens cleaning.",
        expected_outcome_score=80.0,
        expected_outcome_comment="Accurately measures dwell times, but does not directly optimize bus departure timings.",
        scalability_score=87.0,
        scalability_comment="Camera hardware cost increases linearly per bus.",
        security_risk_score=79.0,
        security_risk_comment="Edge face blurring is present, but ongoing camera video privacy audits will be necessary.",
        implementation_readiness_score=84.0,
        implementation_readiness_comment="Hardware installation takes 2-3 days per bus.",
        cost_value_score=80.0,
        cost_value_comment="Hardware-intensive compared to software-first telemetry approaches.",
        total_weighted_score=81.5,
        conflict_of_interest_cleared=True,
        status="submitted",
        overall_recommendation="Conditional Recommendation",
        general_remarks="Useful auxiliary technology for passenger crowding metrics.",
        created_at=datetime.utcnow() - timedelta(days=60),
        submitted_at=datetime.utcnow() - timedelta(days=58)
    )

    db.session.add_all([eval_transit, eval_urbanflow, eval_mobilityvision])
    db.session.commit()

    # 7. Hero Pilot Passport (Ready for Scale status)
    pilot_hero = Pilot(
        code="GP-MH-2026-00421",
        title="PulseTransit: Real-Time Telemetry & Bus Headway Optimization Pilot",
        challenge_id=hero_challenge.id,
        startup_id=startup_transit.id,
        department_id=dept_transport.id,
        application_id=app_transit.id,
        assigned_officer_id=user_gov.id,
        assigned_validator_id=user_validator.id,
        status="ready_for_scale",
        duration_days=90,
        start_date=date.today() - timedelta(days=90),
        end_date=date.today(),
        total_budget=1000000.0,
        disbursed_amount=750000.0,
        test_scope="10 Municipal Transit Buses across 5 High-Density Urban Corridors (Routes 21, 45, 102, 118, 204) with 42 total passenger stops.",
        objectives_summary="Validate AI-driven predictive headway synchronization and real-time dynamic ETA generation to reduce passenger waiting times and eliminate vehicle bunching under peak traffic conditions.",
        success_criteria="1. Average Passenger Waiting Time <= 11.0 min\n2. Commuter App ETA Accuracy >= 92.0%\n3. Route Headway Adherence >= 85.0%\n4. System Telemetry Ingestion Uptime >= 99.5%",
        data_types_shared="Anonymized vehicle AIS-140 GPS coordinates, route timetables, stop geo-fences, live traffic signal cycle status.",
        data_access_level="Confidential / Read-Only Telemetry Sandbox API",
        data_retention_period="90 Days post-pilot audit completion (Raw logs securely archived)",
        data_source="State Urban Transport Command Center (TCC) Telemetry Gateway",
        startup_ip_terms="Pre-existing machine learning models, Kalman filter headway synchronization algorithms, and proprietary prediction weights remain the exclusive intellectual property of TransitAI Labs.",
        government_usage_rights="Government retains perpetual non-exclusive right to pilot performance datasets, benchmarking reports, API integration schemas, and public-facing GTFS-RT data feeds.",
        joint_artifacts="Custom municipal GIS route mapping layers, stop dwell calibration profiles, and API connector schemas.",
        sec_auth_verified=True,
        sec_encryption_verified=True,
        sec_access_control_verified=True,
        sec_logging_verified=True,
        sec_incident_process_verified=True,
        created_at=datetime.utcnow() - timedelta(days=90)
    )

    db.session.add(pilot_hero)
    db.session.commit()

    # 8. Pilot KPIs & Historical Observation Data Points
    kpi1 = PilotKPI(
        pilot_id=pilot_hero.id,
        name="Average Passenger Waiting Time",
        description="Mean duration (in minutes) passengers wait at corridor bus stops before vehicle arrival during peak operating hours (08:00-11:00 and 17:00-20:00).",
        baseline_value=16.4,
        target_value=11.0,
        current_value=10.8,
        unit="minutes",
        higher_is_better=False,
        data_source="Automated Passenger Counter (APC) timestamps & field sample audits",
        measurement_method="Delta between passenger stop arrival time and bus door opening timestamp",
        frequency="Weekly",
        success_threshold="Reduction > 30% from baseline (< 11.5 min)",
        status="Target Achieved"
    )

    kpi2 = PilotKPI(
        pilot_id=pilot_hero.id,
        name="Commuter ETA Prediction Accuracy",
        description="Percentage of real-time arrival predictions accurate within +/- 90 seconds of actual bus arrival across all 42 stops.",
        baseline_value=58.0,
        target_value=92.0,
        current_value=94.2,
        unit="%",
        higher_is_better=True,
        data_source="Live GTFS-RT Telemetry vs Actual Geo-fence Trigger Logs",
        measurement_method="Automated time delta calculation at bus stop boundary entry",
        frequency="Weekly",
        success_threshold="ETA Accuracy >= 90.0%",
        status="Target Achieved"
    )

    kpi3 = PilotKPI(
        pilot_id=pilot_hero.id,
        name="Route Schedule & Headway Adherence",
        description="Percentage of trips maintaining regular vehicle spacing (headway regularity within 15% of target interval), preventing bus bunching.",
        baseline_value=61.2,
        target_value=85.0,
        current_value=89.6,
        unit="%",
        higher_is_better=True,
        data_source="Transit Control Center Headway Dispatch Logs",
        measurement_method="Variance of inter-arrival gaps across consecutive buses on the same route",
        frequency="Weekly",
        success_threshold="Headway Regularity >= 85.0%",
        status="Target Achieved"
    )

    kpi4 = PilotKPI(
        pilot_id=pilot_hero.id,
        name="Central Telemetry System Uptime",
        description="Continuous operational availability of the real-time telemetry ingestion and prediction API pipeline.",
        baseline_value=96.5,
        target_value=99.5,
        current_value=99.9,
        unit="%",
        higher_is_better=True,
        data_source="CloudWatch & Prometheus Telemetry Monitors",
        measurement_method="Synthetic HTTP endpoint pings every 60 seconds",
        frequency="Daily",
        success_threshold="System Uptime >= 99.5%",
        status="Target Achieved"
    )

    db.session.add_all([kpi1, kpi2, kpi3, kpi4])
    db.session.commit()

    # Add 12 Weeks of historical observations for KPI 1 (Waiting Time)
    wait_time_trend = [16.4, 15.8, 15.1, 14.3, 13.6, 12.8, 12.2, 11.7, 11.2, 11.0, 10.9, 10.8]
    for i, val in enumerate(wait_time_trend):
        obs = KPIObservation(
            kpi_id=kpi1.id,
            observation_date=date.today() - timedelta(days=(12-i)*7),
            recorded_value=val,
            period_label=f"Week {i+1}",
            evidence_note=f"Sample size: {1800 + i*150} passenger boarding trips across 5 corridors. Data verified.",
            verified_by_validator=True
        )
        db.session.add(obs)

    # Historical observations for KPI 2 (ETA Accuracy)
    eta_trend = [58.0, 64.5, 71.2, 78.0, 83.4, 87.0, 89.5, 91.2, 92.8, 93.5, 93.9, 94.2]
    for i, val in enumerate(eta_trend):
        obs = KPIObservation(
            kpi_id=kpi2.id,
            observation_date=date.today() - timedelta(days=(12-i)*7),
            recorded_value=val,
            period_label=f"Week {i+1}",
            evidence_note=f"Accuracy calculated over {4500 + i*300} stop arrival events. Automated log verification.",
            verified_by_validator=True
        )
        db.session.add(obs)

    # Historical observations for KPI 3 (Headway Regularity)
    headway_trend = [61.2, 65.0, 69.8, 74.5, 78.2, 81.5, 84.0, 86.2, 87.8, 88.5, 89.1, 89.6]
    for i, val in enumerate(headway_trend):
        obs = KPIObservation(
            kpi_id=kpi3.id,
            observation_date=date.today() - timedelta(days=(12-i)*7),
            recorded_value=val,
            period_label=f"Week {i+1}",
            evidence_note=f"Headway index derived from 10 buses across 5 routes. Zero critical bunching recorded in W12.",
            verified_by_validator=True
        )
        db.session.add(obs)

    # Historical observations for KPI 4 (Uptime)
    uptime_trend = [96.5, 98.2, 99.1, 99.6, 99.8, 99.9, 99.9, 99.8, 99.9, 100.0, 99.9, 99.9]
    for i, val in enumerate(uptime_trend):
        obs = KPIObservation(
            kpi_id=kpi4.id,
            observation_date=date.today() - timedelta(days=(12-i)*7),
            recorded_value=val,
            period_label=f"Week {i+1}",
            evidence_note="Prometheus automated health check log. 0 unplanned outages.",
            verified_by_validator=True
        )
        db.session.add(obs)

    # 9. Pilot Milestones
    m1 = PilotMilestone(
        pilot_id=pilot_hero.id,
        sequence_order=1,
        title="Milestone 1: Telemetry Gateway Ingestion & Bus Fleet Onboarding",
        description="Integrate AIS-140 GPS data streams for 10 test buses into PulseTransit ingestion pipeline with sub-2s latency.",
        due_date=date.today() - timedelta(days=70),
        completion_date=date.today() - timedelta(days=72),
        status="Paid",
        payment_percentage=25.0,
        payment_amount=250000.0,
        deliverables_summary="1. Live telemetry connection to 10 buses.\n2. Ingestion latency benchmark (<1.4s).\n3. Driver tablet mounting and app onboarding.",
        submission_notes="All 10 buses successfully sending AIS-140 GPS packets every 5 seconds. Telemetry latency verified at 1.28s.",
        review_comments="Verified by Transport Department IT cell. Milestone approved for full disbursal.",
        reviewed_by_id=user_gov.id,
        reviewed_at=datetime.utcnow() - timedelta(days=70)
    )

    m2 = PilotMilestone(
        pilot_id=pilot_hero.id,
        sequence_order=2,
        title="Milestone 2: ML Headway Synchronization & Driver Advisory Calibration",
        description="Deploy predictive headway algorithms to regulate bus spacing and eliminate vehicle bunching during morning/evening peak hours.",
        due_date=date.today() - timedelta(days=45),
        completion_date=date.today() - timedelta(days=46),
        status="Paid",
        payment_percentage=25.0,
        payment_amount=250000.0,
        deliverables_summary="1. Trained route speed delay model.\n2. Depot dispatcher advisory console.\n3. Driver holding/spacing advisory notification system.",
        submission_notes="Model trained on 12 months historical logs. In-field driver holding adherence reached 88%. Headway regularity improved to 84%.",
        review_comments="Demonstrated clear reduction in vehicle bunching along Route 21 & 45. Approved.",
        reviewed_by_id=user_gov.id,
        reviewed_at=datetime.utcnow() - timedelta(days=44)
    )

    m3 = PilotMilestone(
        pilot_id=pilot_hero.id,
        sequence_order=3,
        title="Milestone 3: Public GTFS-RT API Integration & Passenger Live ETA Broadcast",
        description="Expose real-time GTFS-RT arrival prediction feeds to the municipal traveler mobile app across all 42 stops.",
        due_date=date.today() - timedelta(days=20),
        completion_date=date.today() - timedelta(days=21),
        status="Paid",
        payment_percentage=25.0,
        payment_amount=250000.0,
        deliverables_summary="1. GTFS-RT feed generator.\n2. Passenger app API integration.\n3. Live ETA accuracy validation at bus stops.",
        submission_notes="GTFS-RT feed live with 94% of arrival predictions within +/- 90 seconds. Over 25,000 passenger queries handled daily.",
        review_comments="Excellent commuter feedback. Independent sample check confirmed high ETA accuracy.",
        reviewed_by_id=user_gov.id,
        reviewed_at=datetime.utcnow() - timedelta(days=19)
    )

    m4 = PilotMilestone(
        pilot_id=pilot_hero.id,
        sequence_order=4,
        title="Milestone 4: Comprehensive Outcome Validation & Scale-Up Dossier Submission",
        description="Complete 90-day pilot execution, submit raw telemetry verification logs, independent audit validation, and draft scale-up roadmap.",
        due_date=date.today(),
        completion_date=date.today() - timedelta(days=2),
        status="Approved",
        payment_percentage=25.0,
        payment_amount=250000.0,
        deliverables_summary="1. Full 90-day outcome analytics report.\n2. Independent validator sign-off dossier.\n3. Architectural blueprint for pan-city 250 bus scale-up.",
        submission_notes="All 4 target KPIs achieved or exceeded. Independent validation completed with zero security non-conformities.",
        review_comments="All deliverables met with high technical rigor. Approved for final milestone disbursal and scale decision.",
        reviewed_by_id=user_gov.id,
        reviewed_at=datetime.utcnow() - timedelta(days=1)
    )

    db.session.add_all([m1, m2, m3, m4])
    db.session.commit()

    # 10. Payments
    p1 = Payment(
        pilot_id=pilot_hero.id,
        milestone_id=m1.id,
        invoice_number="INV-GP-2026-00421-M1",
        amount=250000.0,
        status="Disbursed / Paid",
        disbursed_at=datetime.utcnow() - timedelta(days=68),
        transaction_reference="PFMS-TXN-98421001",
        remarks="Disbursed via Public Financial Management System after Milestone 1 technical sign-off."
    )
    p2 = Payment(
        pilot_id=pilot_hero.id,
        milestone_id=m2.id,
        invoice_number="INV-GP-2026-00421-M2",
        amount=250000.0,
        status="Disbursed / Paid",
        disbursed_at=datetime.utcnow() - timedelta(days=42),
        transaction_reference="PFMS-TXN-98421045",
        remarks="Disbursed after Milestone 2 driver advisory calibration review."
    )
    p3 = Payment(
        pilot_id=pilot_hero.id,
        milestone_id=m3.id,
        invoice_number="INV-GP-2026-00421-M3",
        amount=250000.0,
        status="Disbursed / Paid",
        disbursed_at=datetime.utcnow() - timedelta(days=18),
        transaction_reference="PFMS-TXN-98421092",
        remarks="Disbursed after Milestone 3 GTFS-RT API deployment."
    )
    p4 = Payment(
        pilot_id=pilot_hero.id,
        milestone_id=m4.id,
        invoice_number="INV-GP-2026-00421-M4",
        amount=250000.0,
        status="Department Approved",
        remarks="Milestone 4 approved by CITO. Final payment batch queued for treasury release."
    )
    db.session.add_all([p1, p2, p3, p4])
    db.session.commit()

    # 11. Risks
    r1 = Risk(
        pilot_id=pilot_hero.id,
        title="GPS Urban Canyon Drift in High-Rise Corridor Zones",
        category="Technical",
        severity="Medium",
        probability="Medium",
        owner="Startup (TransitAI)",
        mitigation_strategy="Implemented dead-reckoning map matching algorithm utilizing road segment topology to correct GPS drift.",
        status="Resolved"
    )
    r2 = Risk(
        pilot_id=pilot_hero.id,
        title="Driver Advisory Compliance & Behavioral Adoption",
        category="Operational",
        severity="Medium",
        probability="Low",
        owner="Department & Startup Joint",
        mitigation_strategy="Conducted interactive orientation workshops with bus operators; simplified tablet UI with large visual color cues.",
        status="Resolved"
    )
    r3 = Risk(
        pilot_id=pilot_hero.id,
        title="Telemetry Data Volume Spike during Gridlock Peak Hours",
        category="Technical",
        severity="Low",
        probability="Low",
        owner="Startup (TransitAI)",
        mitigation_strategy="Auto-scaling Redis stream workers deployed in containerized kubernetes cluster.",
        status="Resolved"
    )
    db.session.add_all([r1, r2, r3])
    db.session.commit()

    # 12. Documents
    doc1 = Document(
        pilot_id=pilot_hero.id,
        title="GovPilot Bilateral Innovation Pilot Agreement",
        document_type="Pilot Agreement",
        file_name="GovPilot_Agreement_TransitAI_Signed.pdf",
        file_path="uploads/GovPilot_Agreement_TransitAI_Signed.pdf",
        file_size_kb=420,
        version="v1.0",
        uploaded_by_id=user_gov.id,
        status="Verified"
    )
    doc2 = Document(
        pilot_id=pilot_hero.id,
        title="PulseTransit AI Architecture & Algorithm Whitepaper",
        document_type="Startup Proposal",
        file_name="PulseTransit_System_Architecture_v3.pdf",
        file_path="uploads/PulseTransit_System_Architecture_v3.pdf",
        file_size_kb=850,
        version="v1.2",
        uploaded_by_id=user_startup.id,
        status="Verified"
    )
    doc3 = Document(
        pilot_id=pilot_hero.id,
        title="Data Protection & Telemetry Sharing Sandbox Terms",
        document_type="Data Sharing Agreement",
        file_name="Data_Governance_Protocol_Signed.pdf",
        file_path="uploads/Data_Governance_Protocol_Signed.pdf",
        file_size_kb=310,
        version="v1.0",
        uploaded_by_id=user_gov.id,
        status="Verified"
    )
    doc4 = Document(
        pilot_id=pilot_hero.id,
        title="Independent Technical Audit & Validation Report",
        document_type="Validation Report",
        file_name="Independent_Validation_Report_GP00421.pdf",
        file_path="uploads/Independent_Validation_Report_GP00421.pdf",
        file_size_kb=640,
        version="v1.0",
        uploaded_by_id=user_validator.id,
        status="Verified"
    )
    db.session.add_all([doc1, doc2, doc3, doc4])
    db.session.commit()

    # 13. Independent Validation Report
    val_report = ValidationReport(
        pilot_id=pilot_hero.id,
        validator_id=user_validator.id,
        report_code="VAL-GP-2026-0042",
        status="Completed",
        methodology_reviewed="Independent verification conducted via cross-referencing raw AIS-140 GPS packet stream archives, automated timestamp logs, physical passenger survey ground truth audits at 8 terminal bus stops, and automated synthetic load testing of API endpoints.",
        evidence_sufficiency="High / Sufficient",
        kpi_verification_summary="All 4 target KPIs verified against primary telemetry sources. Average waiting time dropped from 16.4 min to 10.8 min (-34.1%). ETA accuracy within 90s achieved 94.2% (Target: 92.0%). Headway regularity achieved 89.6% (Target: 85.0%). System uptime logged at 99.9%.",
        observations="The solution demonstrated exceptional stability in extreme urban traffic conditions. Driver compliance was high (88%+ adherence). Telemetry processing latency remained consistently under 1.4 seconds. Zero privacy or security vulnerabilities discovered during vulnerability assessment.",
        limitations="Pilot was executed across 10 buses and 5 corridors. Pan-city deployment (250+ buses) will require provisioning additional cloud ingestion worker nodes and integrating with 3 additional bus depot dispatch centers.",
        conclusion="The pilot has conclusively demonstrated technological maturity, operational viability, and measurable public benefit. The solution meets all technical and security criteria for transition to formal statutory procurement.",
        scale_recommendation="Recommend Scale-Up Pathway",
        verified_kpis_count=4,
        total_kpis_count=4,
        created_at=datetime.utcnow() - timedelta(days=5),
        submitted_at=datetime.utcnow() - timedelta(days=3)
    )
    db.session.add(val_report)
    db.session.commit()

    # 14. Scale Decision
    scale_dec = ScaleDecision(
        pilot_id=pilot_hero.id,
        decision_maker_user_id=user_gov.id,
        decision_type="Prepare for Scale",
        target_procurement_pathway="General Financial Rule 149 Innovation Procurement / Open Competitive RFP with Pilot Pre-qualification Technical Standard",
        reasoning="The 90-day pilot achieved a 34.1% reduction in commuter waiting times and 94.2% ETA accuracy with high system reliability (99.9% uptime). Independent validation confirms technical maturity (TRL 8) and positive cost-to-benefit ratio. Expanding the solution across the entire 250-bus fleet will transform municipal transit reliability.",
        supporting_notes="Draft Scale-Up Pack generated containing verified technical specifications, SLA benchmarks, and integration standards for inclusion in the upcoming Pan-City Intelligent Transport System tender.",
        authorized_signatory_name="Rajesh Verma",
        authorized_signatory_title="Chief Innovation & Technology Officer, Urban Transport Authority",
        decision_date=date.today(),
        estimated_scale_budget="₹1,80,00,000 (Pan-City 250 Buses over 24 Months)",
        target_timeline_months=18,
        created_at=datetime.utcnow() - timedelta(days=1)
    )
    db.session.add(scale_dec)
    db.session.commit()

    # 15. Audit Events (Chronological Governance Audit Trail)
    audit_events_data = [
        ("Created Outcome-Based Challenge CH-TRANS-2026-001", "Challenge", "CH-TRANS-2026-001", user_gov, datetime.utcnow() - timedelta(days=96)),
        ("Published Challenge CH-TRANS-2026-001 to Startup Ecosystem", "Challenge", "CH-TRANS-2026-001", user_gov, datetime.utcnow() - timedelta(days=95)),
        ("Startup TransitAI Labs submitted Proposal APP-2026-0042", "Application", "APP-2026-0042", user_startup, datetime.utcnow() - timedelta(days=68)),
        ("Government Officer verified Eligibility Checklist for APP-2026-0042", "Application", "APP-2026-0042", user_gov, datetime.utcnow() - timedelta(days=65)),
        ("Assigned Expert Evaluator Dr. Sunita Mehra to Challenge", "Challenge", "CH-TRANS-2026-001", user_gov, datetime.utcnow() - timedelta(days=63)),
        ("Expert Evaluator completed scoring (Score: 91.2/100, CoI Declared)", "Evaluation", "EVAL-0042", user_expert, datetime.utcnow() - timedelta(days=58)),
        ("Selected TransitAI Labs for Pilot Execution", "Application", "APP-2026-0042", user_gov, datetime.utcnow() - timedelta(days=55)),
        ("Created Pilot Passport GP-MH-2026-00421 (90-Day Sandbox)", "Pilot", "GP-MH-2026-00421", user_gov, datetime.utcnow() - timedelta(days=54)),
        ("Approved Milestone 1 & Disbursed Payment ₹2,50,000", "Milestone", "M1-GP-00421", user_gov, datetime.utcnow() - timedelta(days=70)),
        ("Approved Milestone 2 & Disbursed Payment ₹2,50,000", "Milestone", "M2-GP-00421", user_gov, datetime.utcnow() - timedelta(days=44)),
        ("Approved Milestone 3 & Disbursed Payment ₹2,50,000", "Milestone", "M3-GP-00421", user_gov, datetime.utcnow() - timedelta(days=19)),
        ("Independent Validator completed Validation Report VAL-GP-2026-0042", "ValidationReport", "VAL-GP-2026-0042", user_validator, datetime.utcnow() - timedelta(days=3)),
        ("Authorized Decision: Prepare for Scale (Pan-City 250 Buses)", "ScaleDecision", "SD-GP-00421", user_gov, datetime.utcnow() - timedelta(days=1)),
        ("Generated Official Draft Scale-Up Pack Dossier (PDF)", "ScaleDecision", "GP-MH-2026-00421", user_gov, datetime.utcnow())
    ]

    for action, entity_type, entity_id, u, ts in audit_events_data:
        ev = AuditEvent(
            timestamp=ts,
            user_id=u.id,
            user_email=u.email,
            user_role=u.role,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            ip_address="127.0.0.1",
            details=f"Governance action securely recorded under immutable audit policy for {entity_type} {entity_id}."
        )
        db.session.add(ev)

    # 16. In-App Notifications
    notifs = [
        Notification(
            user_id=user_gov.id,
            title="Pilot Ready for Scale",
            message="Pilot GP-MH-2026-00421 (TransitAI Labs) has achieved 4/4 KPIs and received independent validation sign-off.",
            category="success",
            link_url="/pilots/1"
        ),
        Notification(
            user_id=user_gov.id,
            title="New Startup Application Received",
            message="MobilityVision submitted a new proposal for CH-TRANS-2026-001.",
            category="info",
            link_url="/applications/3"
        ),
        Notification(
            user_id=user_startup.id,
            title="Milestone 4 Approved & Scale Decision Issued",
            message="Congratulations! Your pilot has been marked 'Ready for Scale' and approved for procurement pathway preparation.",
            category="success",
            link_url="/pilots/1"
        ),
        Notification(
            user_id=user_expert.id,
            title="Evaluation Assigned: Emergency Department Triage",
            message="You have been assigned to evaluate 2 startup proposals for Challenge CH-HEALTH-2026-005.",
            category="action",
            link_url="/evaluations"
        ),
        Notification(
            user_id=user_validator.id,
            title="Validation Dossier Completed",
            message="Validation Report VAL-GP-2026-0042 has been successfully archived in the audit register.",
            category="info",
            link_url="/validation"
        )
    ]
    db.session.add_all(notifs)

    db.session.commit()
    print("[GovPilot Seed] Database successfully populated with complete hero demonstration story!")
    return True
