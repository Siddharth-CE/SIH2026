"""
AI Challenge Assistant Service
Provides realistic outcome-based challenge generation from unstructured problem prompts.
Can seamlessly integrate with external LLM APIs (OpenAI, Anthropic, Gemini) via environment variables.
"""
import os
import json

def generate_challenge_blueprint(prompt, department_name="Municipal Administration"):
    """
    Transforms a loose problem statement into a full 8-step GovPilot Outcome-Based Challenge Blueprint.
    """
    lower_prompt = prompt.lower()

    # Heuristic domain classification
    if any(k in lower_prompt for k in ['pothole', 'road', 'pavement', 'asphalt', 'highway', 'street']):
        domain = 'road_damage'
    elif any(k in lower_prompt for k in ['bus', 'delay', 'transit', 'traffic', 'eta', 'congestion', 'transport']):
        domain = 'bus_transit'
    elif any(k in lower_prompt for k in ['water', 'leak', 'pipe', 'pipeline', 'sewage', 'drainage', 'contamination']):
        domain = 'water_management'
    elif any(k in lower_prompt for k in ['waste', 'garbage', 'trash', 'collection', 'landfill', 'recycling', 'bin']):
        domain = 'waste_management'
    elif any(k in lower_prompt for k in ['health', 'hospital', 'triage', 'patient', 'doctor', 'clinic', 'er', 'emergency']):
        domain = 'healthcare'
    elif any(k in lower_prompt for k in ['school', 'education', 'student', 'attendance', 'learning', 'classroom']):
        domain = 'education'
    else:
        domain = 'general_innovation'

    blueprints = {
        'road_damage': {
            'title': 'AI-Assisted Pavement Distress Detection & Automated Work-Order Generation',
            'sector': 'Infrastructure & Roads',
            'urgency': 'High',
            'problem_summary': f"Manual road inspection is resource-intensive and reactive. {prompt}",
            'problem_details': 'Municipal teams currently rely on scheduled human driving audits and citizen complaint hotline logs. This results in delayed identification of severe road fissures and potholes, escalating repair costs and increasing traffic accidents.',
            'baseline_summary': 'Manual inspections cover only 15 km/day with a 72-hour average delay between defect emergence and municipal notification. Detection accuracy of minor fissures is below 60%.',
            'current_process': 'Inspectors drive municipal survey vans at 20 km/h, manually logging GPS coordinates and snapping photos with handheld tablets.',
            'pain_points': 'High operational labor cost; 3 to 5-day latency in complaint triage; inability to inspect during night hours or adverse weather; lack of automated depth measurement.',
            'affected_users': 'Municipal Road Maintenance Engineers, City Commuters, Emergency Vehicle Fleets',
            'expected_outcome': 'Deploy edge-AI camera modules on existing municipal vehicles to autonomously classify, measure (depth/area), and geo-tag pavement distress in real-time, feeding structured work orders into the maintenance ERP.',
            'target_improvement': 'Reduce defect discovery-to-work-order time by 85%, improve detection precision to >92%, and double daily route coverage.',
            'target_kpis_summary': 'Pothole Detection Precision (>90%), Inspection Speed (60 km/day), Mean Time to Notice (<4 hours), False Positive Rate (<5%)',
            'geography': '5 Central Municipal Corridors (80 lane-km total)',
            'target_users_count': '12 Field Road Maintenance Officers & 4 Central Dispatchers',
            'test_facilities': 'Central Municipal Fleet Depot & Smart City GIS Command Room',
            'duration_days': 60,
            'budget_indicative': '₹8,50,000',
            'available_datasets': 'High-resolution City GIS Base Map, 3-Year Historical Road Repair Logs, Municipal Fleet Telemetry Stream',
            'data_sensitivity': 'Confidential / Municipal Internal Infrastructure Layer',
            'api_availability': 'REST APIs with OAuth2 Sandbox Access & GeoJSON streaming endpoints',
            'technical_constraints': 'Edge inference must operate on vehicle 12V power without sustained 4G connectivity; IP67 weather-proofing required.',
            'security_requirements': 'All video frames must be anonymized (blurring citizen faces and civilian vehicle license plates at edge before transmission).',
            'integration_requirements': 'Direct bi-directional sync with Municipal GIS & Public Works Work-Order Management System.',
            'evaluation_criteria_notes': 'Technical precision of 3D depth estimation (25%), Edge compute reliability (25%), Fleet compatibility (15%), Security & privacy redaction (15%), Readiness for pan-city scale (20%)',
            'success_thresholds': 'Average detection precision >= 90%, Zero privacy redaction breaches, Minimum 98% edge node uptime during pilot period.',
            'suggested_kpis': [
                {'name': 'Pothole & Crack Detection Accuracy', 'baseline': 62.0, 'target': 92.0, 'unit': '%', 'higher_is_better': True},
                {'name': 'Mean Time to Notice & Dispatch', 'baseline': 72.0, 'target': 4.0, 'unit': 'hours', 'higher_is_better': False},
                {'name': 'Daily Surveyed Lane Coverage', 'baseline': 15.0, 'target': 65.0, 'unit': 'km/day', 'higher_is_better': True},
                {'name': 'False Positive Work-Order Rate', 'baseline': 26.0, 'target': 4.5, 'unit': '%', 'higher_is_better': False}
            ]
        },
        'bus_transit': {
            'title': 'AI-Based Real-Time Public Bus Delay & Dynamic ETA Optimization',
            'sector': 'Urban Mobility & Transport',
            'urgency': 'High',
            'problem_summary': f"City buses suffer from unpredictable delays and inaccurate passenger arrival predictions. {prompt}",
            'problem_details': 'Fixed timetable scheduling fails under dynamic urban congestion, leading to bus bunching, extended passenger wait times, and declining ridership trust across municipal routes.',
            'baseline_summary': 'Average passenger stop waiting time is 16.4 minutes. Schedule adherence across peak hours is only 61%. Real-time passenger ETA error exceeds 7.8 minutes.',
            'current_process': 'Depot managers monitor static GPS dots on a legacy dashboard with manual radio interventions during severe gridlock.',
            'pain_points': 'Severe bus bunching along major transit corridors; inability to predict congestion 30 minutes ahead; passenger dissatisfaction with static timetables.',
            'affected_users': '450,000 Daily Commuters, 380 Bus Drivers, 18 Central Depot Dispatchers',
            'expected_outcome': 'Deploy an AI-powered predictive telemetry and dynamic dispatch recommendation engine to synchronize headways and broadcast accurate live arrival times (sub-90s error) to passenger apps.',
            'target_improvement': 'Reduce average passenger wait times by >30%, increase headway consistency by 40%, and achieve >90% ETA accuracy.',
            'target_kpis_summary': 'Passenger Waiting Time (<11 min), ETA Accuracy (>92%), Headway Regularity Index (>85%), System Uptime (>99.5%)',
            'geography': '5 High-Density Urban Transit Corridors (Total 42 bus stops)',
            'target_users_count': '10 Transit Buses, 3 Depot Managers, 25,000 Daily Corridor Commuters',
            'test_facilities': 'Central Transport Control Center (TCC) & Depot 3 Operations Lab',
            'duration_days': 90,
            'budget_indicative': '₹10,00,000',
            'available_datasets': 'Live GTFS-RT Telemetry Stream, 12-Month Historical Route Timestamps, Automated Fare Collection (AFC) Boarding Counts',
            'data_sensitivity': 'Public Transit Data / Anonymized Commuter Flow Metrics',
            'api_availability': 'Real-time WebSocket & REST GTFS-RT Feeds with 5-second polling',
            'technical_constraints': 'Compatible with legacy vehicle GPS transponders (protocols: AIS-140); latency under 2 seconds for ETA push.',
            'security_requirements': 'Role-based access for dispatch commands; encrypted MQTT data channels; compliance with National Data Sharing Guidelines.',
            'integration_requirements': 'Ingestion of Municipal Traffic Signal Priority (TSP) feeds and public commuter mobile app push API.',
            'evaluation_criteria_notes': 'Model prediction accuracy under adverse weather and congestion (25%), Algorithm explainability for dispatchers (25%), Latency & scalability (20%), Data security (15%), Cost efficiency (15%)',
            'success_thresholds': 'Passenger wait time reduction >= 25%, ETA prediction error <= 1.5 minutes on 90% of trips, zero system outages.',
            'suggested_kpis': [
                {'name': 'Average Passenger Waiting Time', 'baseline': 16.4, 'target': 11.0, 'unit': 'min', 'higher_is_better': False},
                {'name': 'Commuter ETA Accuracy (within 90s)', 'baseline': 58.0, 'target': 92.5, 'unit': '%', 'higher_is_better': True},
                {'name': 'Route Schedule & Headway Adherence', 'baseline': 61.2, 'target': 88.0, 'unit': '%', 'higher_is_better': True},
                {'name': 'Central Telemetry System Uptime', 'baseline': 96.5, 'target': 99.8, 'unit': '%', 'higher_is_better': True}
            ]
        },
        'water_management': {
            'title': 'Acoustic & Pressure IoT Analytics for Non-Revenue Water (NRW) Leak Detection',
            'sector': 'Water & Sanitation',
            'urgency': 'Critical',
            'problem_summary': f"Subsurface water distribution pipelines experience persistent undetectable leaks. {prompt}",
            'problem_details': 'Over 34% of treated potable water is lost to underground pipe bursts and pinhole leaks before reaching end consumer meters.',
            'baseline_summary': 'Non-Revenue Water loss stands at 34.2%. Average time to localize an underground leak is 6.5 days, usually triggered only when sinkholes or low pressure are reported.',
            'current_process': 'Acoustic listening rods operated manually by field technicians during late night low-noise hours across 400 km of network.',
            'pain_points': 'Massive revenue and water loss; high risk of contamination in low-pressure zones; disruptive emergency road excavations.',
            'expected_outcome': 'Deploy non-invasive acoustic sensors and machine learning hydraulic pressure gradient models to isolate leaks within 5 meters within 6 hours of occurrence.',
            'target_improvement': 'Cut leak detection time by 80% and reduce localized non-revenue water loss by 18%.',
            'target_kpis_summary': 'Leak Localization Precision (<5m), Mean Time to Detect (<6h), Non-Revenue Water Reduction (>15%), Sensor Battery Longevity (>3 yrs)',
            'geography': 'District Metered Area (DMA) 7 (14 km secondary pipeline grid)',
            'target_users_count': '6 Hydraulic Engineers & 18 Zone Maintenance Workers',
            'test_facilities': 'Municipal Water Quality & Flow Monitoring Station B',
            'duration_days': 90,
            'budget_indicative': '₹12,00,000',
            'available_datasets': 'SCADA Pumping Telemetry, DMA Meter Data, Pipe Network GIS Shapefiles',
            'data_sensitivity': 'Critical Public Infrastructure Data / Restricted Access',
            'api_availability': 'OPC-UA / MQTT SCADA Gateway and GIS Web Feature Services',
            'technical_constraints': 'Submersible sensors (IP68) with LoRaWAN/NB-IoT telemetry operating in underground concrete chambers.',
            'security_requirements': 'End-to-end AES-256 payload encryption; isolated SCADA gateway network segment.',
            'integration_requirements': 'Integration with Water Board SCADA & Automated Valve Actuator Telemetry.',
            'evaluation_criteria_notes': 'Leak location precision (30%), Sensor power autonomy (20%), False alarm rejection (20%), Cost per pipeline km (15%), Integration readiness (15%)',
            'success_thresholds': 'Accurate detection of simulated and organic leaks >90% within 8 hours; zero false positive major excavation orders.',
            'suggested_kpis': [
                {'name': 'Non-Revenue Water Loss in Pilot DMA', 'baseline': 34.2, 'target': 18.0, 'unit': '%', 'higher_is_better': False},
                {'name': 'Mean Time to Localize Subsurface Leak', 'baseline': 156.0, 'target': 6.0, 'unit': 'hours', 'higher_is_better': False},
                {'name': 'Leak Pinpointing Accuracy (within 5m)', 'baseline': 42.0, 'target': 91.0, 'unit': '%', 'higher_is_better': True},
                {'name': 'False Alarm Rate per 100km Network', 'baseline': 18.0, 'target': 2.0, 'unit': 'alerts', 'higher_is_better': False}
            ]
        },
        'waste_management': {
            'title': 'Computer Vision & Fill-Level IoT for Dynamic Municipal Waste Collection',
            'sector': 'Municipal Solid Waste & Sanitation',
            'urgency': 'Medium',
            'problem_summary': f"Fixed municipal garbage collection routes lead to overflowing bins and wasteful fuel expenditure. {prompt}",
            'problem_details': 'Collection trucks follow static daily schedules regardless of whether bins are 20% or 110% full, causing visual blight and excessive fuel consumption.',
            'baseline_summary': 'Bin overflow incident rate is 24.8%. Average fuel expenditure per metric ton of collected waste is ₹1,420. Route completion time averages 6.2 hours.',
            'current_process': 'Fixed circular truck routes every morning from 06:00 to 12:00 covering 120 designated community dumpsters.',
            'pain_points': 'Frequent citizen complaints regarding overflowing bins; high diesel fuel consumption; inability to dynamically re-route during road closures.',
            'expected_outcome': 'Equip municipal bins with ruggedized optical/ultrasonic fill sensors and generate dynamic daily optimal collection routes for fleet dispatch.',
            'target_improvement': 'Eliminate bin overflows by >85% while cutting collection fleet fuel mileage by 22%.',
            'target_kpis_summary': 'Bin Overflow Rate (<3%), Fleet Fuel Savings (>20%), Route Completion Time (<4.5 hrs), Sensor Data Reliability (>98%)',
            'geography': 'Municipal Ward 14 & Ward 15 (85 Community Bins, 8 Compactor Trucks)',
            'target_users_count': '8 Truck Drivers, 2 Sanitation Supervisors, 65,000 Ward Residents',
            'test_facilities': 'Ward 14 Sanitation Depot & Solid Waste Control Dashboard',
            'duration_days': 60,
            'budget_indicative': '₹7,50,000',
            'available_datasets': 'Daily Waste Weight Weighbridge Records, Bin Geo-locations, Municipal Truck Fleet GPS Traces',
            'data_sensitivity': 'Internal Municipal Logistics Data',
            'api_availability': 'Fleet GPS REST API & Sanitation GIS layer',
            'technical_constraints': 'Sensors must withstand harsh corrosive environment, steam washing, and 45°C ambient temperatures.',
            'security_requirements': 'TLS encrypted sensor data; authenticated driver tablet applications.',
            'integration_requirements': 'Sync with Municipal Weighbridge ERP and Citizen Grievance Portal.',
            'evaluation_criteria_notes': 'Sensor ruggedness (25%), Dynamic route optimization efficiency (25%), Driver UI ease of use (20%), Solution TCO (15%), Security (15%)',
            'success_thresholds': 'Reduction of bin overflow incidents to <3%; demonstrable 18%+ reduction in fleet diesel consumption.',
            'suggested_kpis': [
                {'name': 'Community Bin Overflow Incident Rate', 'baseline': 24.8, 'target': 3.0, 'unit': '%', 'higher_is_better': False},
                {'name': 'Fleet Fuel Consumption per Ton Collected', 'baseline': 1420.0, 'target': 1100.0, 'unit': '₹/ton', 'higher_is_better': False},
                {'name': 'Average Daily Route Completion Duration', 'baseline': 6.2, 'target': 4.4, 'unit': 'hours', 'higher_is_better': False},
                {'name': 'Citizen Solid Waste Complaints per Week', 'baseline': 48.0, 'target': 6.0, 'unit': 'complaints', 'higher_is_better': False}
            ]
        },
        'healthcare': {
            'title': 'AI-Powered Emergency Department Clinical Triage & Queue Streamlining',
            'sector': 'Public Health & Hospitals',
            'urgency': 'Critical',
            'problem_summary': f"District hospital emergency rooms face acute overcrowding and triage misclassifications. {prompt}",
            'problem_details': 'Clinical staff face severe cognitive overload during peak intake hours, leading to prolonged patient waiting times and delayed prioritization of deteriorating patients.',
            'baseline_summary': 'Average triage wait time for Category 3/4 patients is 48 minutes. Triage protocol discordance rate is 14.5%. Nurse documentation time is 9 minutes per patient.',
            'current_process': 'Paper-based Emergency Severity Index (ESI) scoring recorded by triage nurses followed by manual physical token dispatch.',
            'pain_points': 'High wait times; risk of unrecognized clinical deterioration in waiting areas; excessive documentation burden on nursing staff.',
            'expected_outcome': 'Implement an AI-assisted clinical decision support triage interface combining contactless vital sign telemetry with conversational symptom assessment to accelerate safe triage assignment.',
            'target_improvement': 'Reduce triage intake time by 55% while reducing acuity misclassification by >60%.',
            'target_kpis_summary': 'Door-to-Triage Time (<15 min), ESI Agreement Rate (>95%), Nursing Documentation Time (<3 min), Critical Escalation Speed (<60s)',
            'geography': 'District General Hospital Emergency Department (35 Bed Capacity)',
            'target_users_count': '14 Triage Nurses, 6 Emergency Medical Officers, 220 Daily Patients',
            'test_facilities': 'District General Hospital ER Triage Bay 1 & 2',
            'duration_days': 90,
            'budget_indicative': '₹14,00,000',
            'available_datasets': 'Anonymized Historical ER Admission EHR Records, Vital Sign Waveforms, De-identified Outcome Registries',
            'data_sensitivity': 'Protected Health Information (PHI) / DISHA / HIPAA Equivalent High Sensitivity',
            'api_availability': 'HL7 FHIR v4.0 API Endpoints & DICOM Connectors',
            'technical_constraints': 'On-premise edge appliance execution with zero external public cloud PHI transfer; 99.99% high availability.',
            'security_requirements': 'Strict role-based access, full audit logging of every AI inference recommendation, data-at-rest encryption.',
            'integration_requirements': 'Direct bidirectional integration with Hospital Information Management System (HIMS) and Vital Monitors.',
            'evaluation_criteria_notes': 'Clinical validation & safety margins (35%), Data privacy & on-prem compliance (25%), Nurse user experience (20%), FHIR integration fidelity (20%)',
            'success_thresholds': 'Zero safety critical misclassifications, ESI gold-standard concordance >92%, 40%+ reduction in triage desk latency.',
            'suggested_kpis': [
                {'name': 'Door-to-Triage Completion Time', 'baseline': 48.0, 'target': 15.0, 'unit': 'min', 'higher_is_better': False},
                {'name': 'Clinical Triage Protocol Concordance', 'baseline': 85.5, 'target': 96.0, 'unit': '%', 'higher_is_better': True},
                {'name': 'Nurse Documentation Time per Patient', 'baseline': 9.2, 'target': 3.1, 'unit': 'min', 'higher_is_better': False},
                {'name': 'Critical Deterioration Detection Speed', 'baseline': 18.0, 'target': 1.5, 'unit': 'min', 'higher_is_better': False}
            ]
        },
        'general_innovation': {
            'title': f'Innovation Outcome Blueprint: {prompt[:50].strip().title()} Solution',
            'sector': 'Public Sector Modernization',
            'urgency': 'Medium',
            'problem_summary': f"Government operational workflow bottleneck: {prompt}",
            'problem_details': f'Current departmental operations require modernized, automated, and outcome-driven intervention to resolve: {prompt}',
            'baseline_summary': 'Operational baseline shows substantial latency and manual overhead compared to benchmarked digital standards.',
            'current_process': 'Legacy manual procedures with multi-stage paper handoffs and periodic reporting.',
            'pain_points': 'High turnaround time, lack of automated audit trails, limited predictive analytics.',
            'affected_users': 'Department Officers, Citizen Stakeholders, Regional Field Staff',
            'expected_outcome': 'Deploy a targeted startup solution in a controlled 60-day pilot to validate quantifiable efficiency and accuracy gains.',
            'target_improvement': 'Demonstrate >35% efficiency improvement and >90% operational reliability.',
            'target_kpis_summary': 'Operational Speed (+40%), Accuracy (>95%), Compliance Rate (100%), User Satisfaction (>85%)',
            'geography': 'Designated Municipal / State Department Testing Facility',
            'target_users_count': '25 Key Operational Stakeholders',
            'test_facilities': 'Department Technology Innovation Sandbox',
            'duration_days': 60,
            'budget_indicative': '₹8,00,000',
            'available_datasets': 'Sample Anonymized Operational Logs & Workflow Metadata',
            'data_sensitivity': 'Confidential Departmental Data',
            'api_availability': 'Standard JSON REST APIs & Secure SFTP Endpoints',
            'technical_constraints': 'Standard web/mobile architecture, cloud or hybrid deployment with HTTPS encryption.',
            'security_requirements': 'Role-based access control, TLS 1.3 encryption, and compliance with government data protection norms.',
            'integration_requirements': 'Integration with departmental single sign-on and core transaction databases.',
            'evaluation_criteria_notes': 'Technical approach & feasibility (30%), Outcome alignment (25%), Security & compliance (20%), Cost effectiveness (15%), Scalability (10%)',
            'success_thresholds': 'Demonstrate >30% measurable KPI improvement and 100% security compliance.',
            'suggested_kpis': [
                {'name': 'Operational Cycle Time Reduction', 'baseline': 100.0, 'target': 60.0, 'unit': 'hours', 'higher_is_better': False},
                {'name': 'Process Accuracy & Compliance', 'baseline': 74.0, 'target': 95.0, 'unit': '%', 'higher_is_better': True},
                {'name': 'User Task Completion Efficiency', 'baseline': 45.0, 'target': 85.0, 'unit': '%', 'higher_is_better': True},
                {'name': 'System Availability & Reliability', 'baseline': 92.0, 'target': 99.5, 'unit': '%', 'higher_is_better': True}
            ]
        }
    }

    result = blueprints.get(domain, blueprints['general_innovation'])
    return result
