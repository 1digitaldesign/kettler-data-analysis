# Documentation Graph

Complete graph of all documentation files and their relationships.

```mermaid
graph TB
    subgraph "OTHER"
        CODE_FIXES_SUMMARY_md["CODE_FIXES_SUMMARY"]
        INSTALL_PYTHON_3_14_md["INSTALL_PYTHON_3.14"]
        INVESTIGATION_READY_md["INVESTIGATION_READY"]
        SUMMARY_md["SUMMARY"]
        scripts_README_md["README"]
        scripts_automation_BROWSER_AUTOMATION_TROUBLESHOOTING_md["BROWSER_AUTOMATION_TROUBLESHOOTING"]
        scripts_automation_EXPANSION_COMPLETE_md["EXPANSION_COMPLETE"]
        scripts_automation_README_md["README"]
        scripts_automation_README_DEVTOOLS_md["README_DEVTOOLS"]
        scripts_automation_UNIVERSAL_SCRAPER_GUIDE_md["UNIVERSAL_SCRAPER_GUIDE"]
        scripts_automation_devtools_scraping_guide_md["devtools_scraping_guide"]
    end
    subgraph "ROOT"
        INSTALLATION_md["INSTALLATION"]
        QUICK_START_md["QUICK_START"]
        README_md["README"]
        STATUS_md["STATUS"]
    end
    subgraph "DATA"
        data_ANCESTRY_md["ANCESTRY"]
        data_DATA_CATALOG_md["DATA_CATALOG"]
        data_DATA_DICTIONARY_md["DATA_DICTIONARY"]
        data_GOVERNANCE_md["GOVERNANCE"]
        data_ONTOLOGY_md["ONTOLOGY"]
        data_README_md["README"]
    end
    subgraph "SYSTEM"
        docs_ARCHIVE_md["ARCHIVE"]
        docs_DEPLOYMENT_md["DEPLOYMENT"]
        docs_DOCUMENTATION_ARCHITECTURE_VERIFICATION_md["DOCUMENTATION_ARCHITECTURE_VERIFICATION"]
        docs_DOCUMENTATION_GRAPH_md["DOCUMENTATION_GRAPH"]
        docs_INDEX_md["INDEX"]
        docs_NAMING_CONVENTIONS_md["NAMING_CONVENTIONS"]
        docs_REPOSITORY_STRUCTURE_md["REPOSITORY_STRUCTURE"]
        docs_SYSTEM_ARCHITECTURE_md["SYSTEM_ARCHITECTURE"]
        docs_archive_COMPLETE_md["COMPLETE"]
        docs_archive_COMPLETE_INVESTIGATION_STATUS_md["COMPLETE_INVESTIGATION_STATUS"]
        docs_archive_COMPONENTS_md["COMPONENTS"]
        docs_archive_DATA_FLOW_md["DATA_FLOW"]
        docs_archive_DIAGRAMS_md["DIAGRAMS"]
        docs_archive_FINAL_INVESTIGATION_REPORT_md["FINAL_INVESTIGATION_REPORT"]
        docs_archive_FINAL_STATUS_md["FINAL_STATUS"]
        docs_archive_INVESTIGATION_COMPLETE_md["INVESTIGATION_COMPLETE"]
        docs_archive_INVESTIGATION_COMPLETE_FINAL_md["INVESTIGATION_COMPLETE_FINAL"]
        docs_archive_INVESTIGATION_COMPLETE_SUMMARY_md["INVESTIGATION_COMPLETE_SUMMARY"]
        docs_archive_INVESTIGATION_FINAL_STATUS_md["INVESTIGATION_FINAL_STATUS"]
        docs_archive_INVESTIGATION_PACKAGE_COMPLETE_md["INVESTIGATION_PACKAGE_COMPLETE"]
        docs_archive_INVESTIGATION_STATUS_FINAL_md["INVESTIGATION_STATUS_FINAL"]
        docs_archive_MICROSERVICES_IMPLEMENTATION_COMPLETE_md["MICROSERVICES_IMPLEMENTATION_COMPLETE"]
        docs_archive_ORGANIZATION_md["ORGANIZATION"]
        docs_archive_REPOSITORY_REORGANIZATION_COMPLETE_md["REPOSITORY_REORGANIZATION_COMPLETE"]
    end
    subgraph "GUIDE"
        docs_SYSTEM_ANALYST_GUIDE_md["SYSTEM_ANALYST_GUIDE"]
    end
    subgraph "RESEARCH"
        research_ARCHIVE_md["ARCHIVE"]
        research_COMPLAINT_AMENDMENT_GUIDE_md["COMPLAINT_AMENDMENT_GUIDE"]
        research_DATA_GUIDE_md["DATA_GUIDE"]
        research_EVIDENCE_INDEX_md["EVIDENCE_INDEX"]
        research_EXECUTIVE_SUMMARY_md["EXECUTIVE_SUMMARY"]
        research_HANDOFF_DOCUMENT_md["HANDOFF_DOCUMENT"]
        research_MASTER_INDEX_md["MASTER_INDEX"]
        research_QUICK_START_md["QUICK_START"]
        research_README_md["README"]
        research_REPORTS_md["REPORTS"]
        research_archive_COMPLETE_INVESTIGATION_SUMMARY_md["COMPLETE_INVESTIGATION_SUMMARY"]
        research_archive_COMPLETE_PACKAGE_SUMMARY_md["COMPLETE_PACKAGE_SUMMARY"]
        research_archive_EXECUTION_SUMMARY_md["EXECUTION_SUMMARY"]
        research_archive_FINAL_DELIVERABLES_SUMMARY_md["FINAL_DELIVERABLES_SUMMARY"]
        research_archive_FINAL_STATUS_RECONCILIATION_md["FINAL_STATUS_RECONCILIATION"]
        research_archive_FINAL_VERIFICATION_REPORT_md["FINAL_VERIFICATION_REPORT"]
        research_archive_FINDINGS_VALIDATION_REPORT_md["FINDINGS_VALIDATION_REPORT"]
        research_archive_INVESTIGATION_COMPLETE_GUIDE_md["INVESTIGATION_COMPLETE_GUIDE"]
        research_archive_INVESTIGATION_STATISTICS_md["INVESTIGATION_STATISTICS"]
        research_archive_INVESTIGATION_STATUS_COMPLETE_md["INVESTIGATION_STATUS_COMPLETE"]
        research_archive_MASTER_INVESTIGATION_STATUS_md["MASTER_INVESTIGATION_STATUS"]
        research_archive_MASTER_RESEARCH_COMPLETION_REPORT_md["MASTER_RESEARCH_COMPLETION_REPORT"]
        research_archive_PROJECT_COMPLETE_md["PROJECT_COMPLETE"]
        research_archive_STATUS_FILES_ARCHIVE_md["STATUS_FILES_ARCHIVE"]
        research_archive_VALIDATION_REPORT_md["VALIDATION_REPORT"]
        research_archive_VIRGINIA_EXTRACTION_COMPLETE_SUMMARY_md["VIRGINIA_EXTRACTION_COMPLETE_SUMMARY"]
        research_archive_VIRGINIA_EXTRACTION_FINAL_STATUS_md["VIRGINIA_EXTRACTION_FINAL_STATUS"]
        research_archive_VIRGINIA_EXTRACTION_STATUS_md["VIRGINIA_EXTRACTION_STATUS"]
        research_archive_VIRGINIA_EXTRACTION_SUMMARY_md["VIRGINIA_EXTRACTION_SUMMARY"]
        research_browser_automation_DATABASE_SEARCH_FRAMEWORK_md["DATABASE_SEARCH_FRAMEWORK"]
        research_browser_automation_README_md["README"]
        research_investigations_README_md["README"]
        research_investigations_hyland_upl_evidence_md["hyland-upl-evidence"]
        research_investigations_kettler_operational_locations_md["kettler-operational-locations"]
        research_investigations_lariat_affiliated_companies_investigation_md["lariat-affiliated-companies-investigation"]
        research_investigations_lariat_affiliated_companies_summary_md["lariat-affiliated-companies-summary"]
        research_investigations_lariat_broker_for_rent_analysis_md["lariat-broker-for-rent-analysis"]
        research_investigations_lariat_companies_findings_md["lariat-companies-findings"]
        research_investigations_lariat_companies_search_md["lariat-companies-search"]
        research_investigations_lariat_vs_kettler_licensing_strategy_md["lariat-vs-kettler-licensing-strategy"]
        research_investigations_method_comparison_md["method-comparison"]
        research_investigations_moore_kristen_jones_investigation_md["moore-kristen-jones-investigation"]
        research_investigations_remaining_legal_violations_md["remaining-legal-violations"]
        research_investigations_virginia_40_licenses_finding_md["virginia-40-licenses-finding"]
        research_investigations_virginia_companies_found_md["virginia-companies-found"]
        research_license_searches_100_PERCENT_COVERAGE_CONFIRMED_md["100_PERCENT_COVERAGE_CONFIRMED"]
        research_license_searches_KEY_FINDINGS_DC_md["KEY_FINDINGS_DC"]
        research_license_searches_LEAH_DOUTHIT_LIDDY_BISANZ_SEARCH_PLAN_md["LEAH_DOUTHIT_LIDDY_BISANZ_SEARCH_PLAN"]
        research_license_searches_LICENSE_SEARCHES_COMPLETE_md["LICENSE_SEARCHES_COMPLETE"]
        research_license_searches_LICENSE_SEARCHES_FINAL_COMPLETE_md["LICENSE_SEARCHES_FINAL_COMPLETE"]
        research_license_searches_README_md["README"]
        research_license_searches_READY_FOR_FILINGS_md["READY_FOR_FILINGS"]
        research_license_searches_REORGANIZATION_AND_PROGRESS_md["REORGANIZATION_AND_PROGRESS"]
        research_license_searches_REORGANIZATION_COMPLETE_md["REORGANIZATION_COMPLETE"]
        research_license_searches_ROBERT_KETTLER_SUMMARY_md["ROBERT_KETTLER_SUMMARY"]
        research_license_searches_SEAN_CURTIN_BAR_LICENSE_SEARCH_md["SEAN_CURTIN_BAR_LICENSE_SEARCH"]
        research_license_searches_UNLICENSED_OPERATIONS_REPORT_md["UNLICENSED_OPERATIONS_REPORT"]
        research_license_searches_archive_BATCH_SEARCH_PROGRESS_md["BATCH_SEARCH_PROGRESS"]
        research_license_searches_archive_CURRENT_PROGRESS_UPDATE_md["CURRENT_PROGRESS_UPDATE"]
        research_license_searches_archive_CURRENT_SEARCH_STATUS_md["CURRENT_SEARCH_STATUS"]
        research_license_searches_archive_CURRENT_STATUS_md["CURRENT_STATUS"]
        research_license_searches_archive_CURRENT_STATUS_SUMMARY_md["CURRENT_STATUS_SUMMARY"]
        research_license_searches_archive_FINAL_BATCH_PROGRESS_md["FINAL_BATCH_PROGRESS"]
        research_license_searches_archive_FINAL_COMPLETION_SUMMARY_md["FINAL_COMPLETION_SUMMARY"]
        research_license_searches_archive_FINAL_INVESTIGATION_STATUS_md["FINAL_INVESTIGATION_STATUS"]
        research_license_searches_archive_FINAL_INVESTIGATION_SUMMARY_md["FINAL_INVESTIGATION_SUMMARY"]
        research_license_searches_archive_FINAL_STATUS_REPORT_md["FINAL_STATUS_REPORT"]
        research_license_searches_archive_INVESTIGATION_COMPLETE_REPORT_md["INVESTIGATION_COMPLETE_REPORT"]
        research_license_searches_archive_INVESTIGATION_COMPLETE_SUMMARY_md["INVESTIGATION_COMPLETE_SUMMARY"]
        research_license_searches_archive_INVESTIGATION_STATUS_UPDATE_md["INVESTIGATION_STATUS_UPDATE"]
        research_license_searches_archive_LATEST_FINDINGS_UPDATE_md["LATEST_FINDINGS_UPDATE"]
        research_license_searches_archive_PROGRESS_SUMMARY_FINAL_md["PROGRESS_SUMMARY_FINAL"]
        research_license_searches_archive_PROGRESS_UPDATE_md["PROGRESS_UPDATE"]
        research_license_searches_archive_REMAINING_WORK_SUMMARY_md["REMAINING_WORK_SUMMARY"]
        research_license_searches_archive_SEARCH_PROGRESS_UPDATE_md["SEARCH_PROGRESS_UPDATE"]
        research_license_searches_archive_completion_status_ALL_FINDINGS_SUMMARY_md["ALL_FINDINGS_SUMMARY"]
        research_license_searches_archive_completion_status_AUTOMATION_READY_md["AUTOMATION_READY"]
        research_license_searches_archive_completion_status_CAITLIN_SKIDMORE_MULTI_STATE_md["CAITLIN_SKIDMORE_MULTI_STATE"]
        research_license_searches_archive_completion_status_COMPLETE_OPERATIONAL_STATES_SEARCH_md["COMPLETE_OPERATIONAL_STATES_SEARCH"]
        research_license_searches_archive_completion_status_COMPREHENSIVE_FINAL_STATUS_md["COMPREHENSIVE_FINAL_STATUS"]
        research_license_searches_archive_completion_status_COMPREHENSIVE_PROGRESS_md["COMPREHENSIVE_PROGRESS"]
        research_license_searches_archive_completion_status_CONSOLIDATED_FINDINGS_SUMMARY_md["CONSOLIDATED_FINDINGS_SUMMARY"]
        research_license_searches_archive_completion_status_CORE_15_EMPLOYEES_LIST_md["CORE_15_EMPLOYEES_LIST"]
        research_license_searches_archive_completion_status_CRITICAL_PATTERN_UPDATE_md["CRITICAL_PATTERN_UPDATE"]
        research_license_searches_archive_completion_status_DATA_VERIFICATION_FINAL_md["DATA_VERIFICATION_FINAL"]
        research_license_searches_archive_completion_status_DMV_COMPLETENESS_VERIFICATION_md["DMV_COMPLETENESS_VERIFICATION"]
        research_license_searches_archive_completion_status_DMV_FINAL_STATUS_md["DMV_FINAL_STATUS"]
        research_license_searches_archive_completion_status_FINAL_COMPREHENSIVE_STATUS_md["FINAL_COMPREHENSIVE_STATUS"]
        research_license_searches_archive_completion_status_FINAL_REORGANIZATION_SUMMARY_md["FINAL_REORGANIZATION_SUMMARY"]
        research_license_searches_archive_completion_status_FINAL_VALIDATION_SUMMARY_md["FINAL_VALIDATION_SUMMARY"]
        research_license_searches_archive_completion_status_ISSUES_ENCOUNTERED_md["ISSUES_ENCOUNTERED"]
        research_license_searches_archive_completion_status_KEY_FINDINGS_COMPREHENSIVE_md["KEY_FINDINGS_COMPREHENSIVE"]
        research_license_searches_archive_completion_status_LATEST_BATCH_RESULTS_md["LATEST_BATCH_RESULTS"]
        research_license_searches_archive_completion_status_LATEST_FINDINGS_md["LATEST_FINDINGS"]
        research_license_searches_archive_completion_status_NEXT_STEPS_md["NEXT_STEPS"]
        research_license_searches_archive_completion_status_NJ_NY_COMPLETE_SUMMARY_md["NJ_NY_COMPLETE_SUMMARY"]
        research_license_searches_archive_completion_status_SEARCH_COMPLETION_STATUS_md["SEARCH_COMPLETION_STATUS"]
        research_license_searches_archive_completion_status_SEARCH_COMPLETION_SUMMARY_md["SEARCH_COMPLETION_SUMMARY"]
        research_license_searches_archive_completion_status_SUMMARY_AND_STATUS_md["SUMMARY_AND_STATUS"]
        research_license_searches_archive_completion_status_THOMAS_BISANZ_SEARCH_COMPLETE_md["THOMAS_BISANZ_SEARCH_COMPLETE"]
        research_license_searches_archive_completion_status_URLS_AND_PROGRESS_md["URLS_AND_PROGRESS"]
        research_license_searches_archive_completion_status_VALIDATION_REPORT_md["VALIDATION_REPORT"]
        research_license_searches_archive_completion_status_VERIFICATION_COMPLETE_md["VERIFICATION_COMPLETE"]
        research_license_searches_data_connecticut_BROWSER_AUTOMATION_EXECUTED_md["BROWSER_AUTOMATION_EXECUTED"]
        research_license_searches_data_connecticut_CONNECTICUT_SEARCH_STATUS_md["CONNECTICUT_SEARCH_STATUS"]
        research_license_searches_data_dc_DC_SEARCH_COMPLETE_md["DC_SEARCH_COMPLETE"]
        research_license_searches_data_maryland_ADDITIONAL_MARYLAND_SEARCHES_md["ADDITIONAL_MARYLAND_SEARCHES"]
        research_license_searches_data_maryland_CAPTCHA_BYPASS_OPTIONS_md["CAPTCHA_BYPASS_OPTIONS"]
        research_license_searches_data_maryland_CAPTCHA_REQUIRED_md["CAPTCHA_REQUIRED"]
        research_license_searches_data_maryland_CAPTCHA_SERVICE_SETUP_md["CAPTCHA_SERVICE_SETUP"]
        research_license_searches_data_maryland_IMPLEMENTATION_STATUS_md["IMPLEMENTATION_STATUS"]
        research_license_searches_data_maryland_MANUAL_CAPTCHA_INSTRUCTIONS_md["MANUAL_CAPTCHA_INSTRUCTIONS"]
        research_license_searches_data_maryland_MANUAL_SEARCH_CHECKLIST_md["MANUAL_SEARCH_CHECKLIST"]
        research_license_searches_data_maryland_MARYLAND_CAPTCHA_SOLUTION_SUMMARY_md["MARYLAND_CAPTCHA_SOLUTION_SUMMARY"]
        research_license_searches_data_maryland_MARYLAND_FINDINGS_SUMMARY_md["MARYLAND_FINDINGS_SUMMARY"]
        research_license_searches_data_maryland_MARYLAND_LICENSED_EMPLOYEES_UPDATE_md["MARYLAND_LICENSED_EMPLOYEES_UPDATE"]
        research_license_searches_data_maryland_MARYLAND_PROGRESS_md["MARYLAND_PROGRESS"]
        research_license_searches_data_maryland_MARYLAND_SEARCH_STATUS_md["MARYLAND_SEARCH_STATUS"]
        research_license_searches_data_maryland_MARYLAND_SEARCH_STRATEGY_md["MARYLAND_SEARCH_STRATEGY"]
        research_license_searches_data_maryland_SETUP_CAPTCHA_SERVICE_md["SETUP_CAPTCHA_SERVICE"]
        research_license_searches_reports_ACTION_PLAN_md["ACTION_PLAN"]
        research_license_searches_reports_ADMINISTRATIVE_FILING_CHECKLIST_md["ADMINISTRATIVE_FILING_CHECKLIST"]
        research_license_searches_reports_COMPLETE_INVESTIGATION_PACKAGE_md["COMPLETE_INVESTIGATION_PACKAGE"]
        research_license_searches_reports_COMPREHENSIVE_VIOLATIONS_REPORT_md["COMPREHENSIVE_VIOLATIONS_REPORT"]
        research_license_searches_reports_EXECUTIVE_SUMMARY_FOR_FILINGS_md["EXECUTIVE_SUMMARY_FOR_FILINGS"]
        research_license_searches_reports_INVESTIGATION_SUMMARY_md["INVESTIGATION_SUMMARY"]
        research_license_searches_reports_MASTER_INVESTIGATION_REPORT_md["MASTER_INVESTIGATION_REPORT"]
        research_license_searches_reports_QUICK_REFERENCE_md["QUICK_REFERENCE"]
        research_reports_ALL_ANOMALIES_SUMMARY_md["ALL_ANOMALIES_SUMMARY"]
        research_reports_ALL_VIOLATIONS_AND_ANOMALIES_md["ALL_VIOLATIONS_AND_ANOMALIES"]
        research_reports_COMPLETE_AUDIT_SUMMARY_md["COMPLETE_AUDIT_SUMMARY"]
        research_reports_COMPREHENSIVE_ANOMALIES_REPORT_md["COMPREHENSIVE_ANOMALIES_REPORT"]
        research_reports_COMPREHENSIVE_VIOLATIONS_REPORT_md["COMPREHENSIVE_VIOLATIONS_REPORT"]
        research_reports_FINAL_NEXUS_FINDINGS_md["FINAL_NEXUS_FINDINGS"]
        research_reports_FINAL_VIOLATION_SUMMARY_md["FINAL_VIOLATION_SUMMARY"]
        research_reports_NEXUS_ANALYSIS_REPORT_md["NEXUS_ANALYSIS_REPORT"]
        research_reports_RESEARCH_COMPLETION_SUMMARY_md["RESEARCH_COMPLETION_SUMMARY"]
        research_reports_VIOLATION_AUDIT_COMPLETE_md["VIOLATION_AUDIT_COMPLETE"]
        research_reports_validation_report_md["validation_report"]
        research_va_dpor_complaint_evidence_exhibits_compilation_md["evidence_exhibits_compilation"]
    end
    INSTALLATION_md --> QUICK_START_md
    INSTALLATION_md --> README_md
    INSTALLATION_md --> docs_SYSTEM_ARCHITECTURE_md
    INSTALLATION_md --> QUICK_START_md
    INSTALLATION_md --> docs_SYSTEM_ARCHITECTURE_md
    INSTALLATION_md --> docs_INDEX_md
    INSTALL_PYTHON_3_14_md --> INSTALLATION_md
    INSTALL_PYTHON_3_14_md --> QUICK_START_md
    QUICK_START_md --> INSTALLATION_md
    QUICK_START_md --> README_md
    QUICK_START_md --> docs_SYSTEM_ARCHITECTURE_md
    QUICK_START_md --> INSTALLATION_md
    QUICK_START_md --> docs_SYSTEM_ARCHITECTURE_md
    QUICK_START_md --> docs_INDEX_md
    QUICK_START_md --> INSTALLATION_md
    QUICK_START_md --> docs_SYSTEM_ARCHITECTURE_md
    QUICK_START_md --> docs_INDEX_md
    README_md --> research_README_md
    README_md --> INSTALLATION_md
    README_md --> INSTALLATION_md
    README_md --> QUICK_START_md
    README_md --> STATUS_md
    README_md --> docs_SYSTEM_ARCHITECTURE_md
    README_md --> docs_REPOSITORY_STRUCTURE_md
    README_md --> docs_SYSTEM_ANALYST_GUIDE_md
    README_md --> data_DATA_DICTIONARY_md
    README_md --> data_ONTOLOGY_md
    README_md --> data_ANCESTRY_md
    README_md --> data_DATA_CATALOG_md
    README_md --> data_GOVERNANCE_md
    README_md --> docs_INDEX_md
    README_md --> docs_DOCUMENTATION_GRAPH_md
    STATUS_md --> README_md
    STATUS_md --> research_README_md
    STATUS_md --> data_README_md
    STATUS_md --> docs_INDEX_md
    data_ANCESTRY_md --> data_DATA_CATALOG_md
    data_ANCESTRY_md --> data_GOVERNANCE_md
    data_ANCESTRY_md --> data_DATA_DICTIONARY_md
    data_ANCESTRY_md --> data_ONTOLOGY_md
    data_ANCESTRY_md --> data_README_md
    data_ANCESTRY_md --> docs_INDEX_md
    data_ANCESTRY_md --> docs_SYSTEM_ARCHITECTURE_md
    data_ANCESTRY_md --> docs_REPOSITORY_STRUCTURE_md
    data_DATA_CATALOG_md --> data_DATA_DICTIONARY_md
    data_DATA_CATALOG_md --> data_ONTOLOGY_md
    data_DATA_CATALOG_md --> data_ANCESTRY_md
    data_DATA_CATALOG_md --> data_ANCESTRY_md
    data_DATA_CATALOG_md --> data_DATA_DICTIONARY_md
    data_DATA_CATALOG_md --> data_ONTOLOGY_md
    data_DATA_CATALOG_md --> data_ANCESTRY_md
    data_DATA_CATALOG_md --> data_DATA_DICTIONARY_md
    data_DATA_CATALOG_md --> data_ONTOLOGY_md
    data_DATA_CATALOG_md --> data_ANCESTRY_md
    data_DATA_CATALOG_md --> data_GOVERNANCE_md
    data_DATA_CATALOG_md --> data_README_md
    data_DATA_CATALOG_md --> docs_INDEX_md
    data_DATA_CATALOG_md --> docs_SYSTEM_ARCHITECTURE_md
    data_DATA_CATALOG_md --> docs_SYSTEM_ANALYST_GUIDE_md
    data_DATA_CATALOG_md --> docs_REPOSITORY_STRUCTURE_md
    data_DATA_DICTIONARY_md --> data_DATA_CATALOG_md
    data_DATA_DICTIONARY_md --> data_GOVERNANCE_md
    data_DATA_DICTIONARY_md --> data_ONTOLOGY_md
    data_DATA_DICTIONARY_md --> data_ANCESTRY_md
    data_DATA_DICTIONARY_md --> data_README_md
    data_DATA_DICTIONARY_md --> docs_INDEX_md
    data_DATA_DICTIONARY_md --> docs_SYSTEM_ARCHITECTURE_md
    data_DATA_DICTIONARY_md --> docs_REPOSITORY_STRUCTURE_md
    data_GOVERNANCE_md --> data_DATA_CATALOG_md
    data_GOVERNANCE_md --> data_DATA_DICTIONARY_md
    data_GOVERNANCE_md --> data_ONTOLOGY_md
    data_GOVERNANCE_md --> data_ANCESTRY_md
    data_GOVERNANCE_md --> data_README_md
    data_GOVERNANCE_md --> docs_INDEX_md
    data_GOVERNANCE_md --> docs_SYSTEM_ARCHITECTURE_md
    data_GOVERNANCE_md --> docs_SYSTEM_ANALYST_GUIDE_md
    data_GOVERNANCE_md --> docs_REPOSITORY_STRUCTURE_md
    data_ONTOLOGY_md --> data_DATA_DICTIONARY_md
    data_ONTOLOGY_md --> data_DATA_CATALOG_md
    data_ONTOLOGY_md --> data_GOVERNANCE_md
    data_ONTOLOGY_md --> data_DATA_DICTIONARY_md
    data_ONTOLOGY_md --> data_ANCESTRY_md
    data_ONTOLOGY_md --> data_README_md
    data_ONTOLOGY_md --> docs_INDEX_md
    data_ONTOLOGY_md --> docs_SYSTEM_ARCHITECTURE_md
    data_ONTOLOGY_md --> docs_REPOSITORY_STRUCTURE_md
    data_README_md --> data_DATA_CATALOG_md
    data_README_md --> data_GOVERNANCE_md
    data_README_md --> data_DATA_DICTIONARY_md
    data_README_md --> data_ONTOLOGY_md
    data_README_md --> data_ANCESTRY_md
    data_README_md --> data_DATA_CATALOG_md
    data_README_md --> data_DATA_DICTIONARY_md
    data_README_md --> data_ANCESTRY_md
    data_README_md --> data_ONTOLOGY_md
    data_README_md --> data_GOVERNANCE_md
    data_README_md --> data_DATA_CATALOG_md
    data_README_md --> research_README_md
    data_README_md --> docs_REPOSITORY_STRUCTURE_md
    docs_ARCHIVE_md --> STATUS_md
    docs_ARCHIVE_md --> STATUS_md
    docs_ARCHIVE_md --> README_md
    docs_ARCHIVE_md --> docs_INDEX_md
    docs_INDEX_md --> docs_DOCUMENTATION_GRAPH_md
    docs_INDEX_md --> README_md
    docs_INDEX_md --> INSTALLATION_md
    docs_INDEX_md --> QUICK_START_md
    docs_INDEX_md --> STATUS_md
    docs_INDEX_md --> docs_SYSTEM_ARCHITECTURE_md
    docs_INDEX_md --> docs_REPOSITORY_STRUCTURE_md
    docs_INDEX_md --> docs_SYSTEM_ANALYST_GUIDE_md
    docs_INDEX_md --> docs_DEPLOYMENT_md
    docs_INDEX_md --> docs_ARCHIVE_md
    docs_INDEX_md --> docs_NAMING_CONVENTIONS_md
    docs_INDEX_md --> docs_DOCUMENTATION_ARCHITECTURE_VERIFICATION_md
    docs_INDEX_md --> data_DATA_DICTIONARY_md
    docs_INDEX_md --> data_ONTOLOGY_md
    docs_INDEX_md --> data_ANCESTRY_md
    docs_INDEX_md --> data_DATA_CATALOG_md
    docs_INDEX_md --> data_GOVERNANCE_md
    docs_INDEX_md --> data_README_md
    docs_INDEX_md --> research_README_md
    docs_INDEX_md --> docs_DEPLOYMENT_md
    docs_INDEX_md --> docs_DOCUMENTATION_GRAPH_md
    docs_NAMING_CONVENTIONS_md --> docs_REPOSITORY_STRUCTURE_md
    docs_NAMING_CONVENTIONS_md --> data_DATA_DICTIONARY_md
    docs_NAMING_CONVENTIONS_md --> docs_SYSTEM_ARCHITECTURE_md
    docs_REPOSITORY_STRUCTURE_md --> docs_SYSTEM_ARCHITECTURE_md
    docs_SYSTEM_ANALYST_GUIDE_md --> data_DATA_CATALOG_md
    docs_SYSTEM_ANALYST_GUIDE_md --> data_GOVERNANCE_md
    docs_SYSTEM_ANALYST_GUIDE_md --> docs_SYSTEM_ARCHITECTURE_md
    docs_SYSTEM_ANALYST_GUIDE_md --> docs_SYSTEM_ARCHITECTURE_md
    docs_SYSTEM_ANALYST_GUIDE_md --> docs_REPOSITORY_STRUCTURE_md
    docs_SYSTEM_ARCHITECTURE_md --> data_DATA_DICTIONARY_md
    docs_SYSTEM_ARCHITECTURE_md --> data_DATA_CATALOG_md
    docs_SYSTEM_ARCHITECTURE_md --> data_GOVERNANCE_md
    docs_SYSTEM_ARCHITECTURE_md --> data_DATA_DICTIONARY_md
    docs_SYSTEM_ARCHITECTURE_md --> data_DATA_CATALOG_md
    docs_SYSTEM_ARCHITECTURE_md --> data_GOVERNANCE_md
    docs_SYSTEM_ARCHITECTURE_md --> docs_INDEX_md
    docs_SYSTEM_ARCHITECTURE_md --> docs_REPOSITORY_STRUCTURE_md
    docs_SYSTEM_ARCHITECTURE_md --> docs_DOCUMENTATION_GRAPH_md
    docs_archive_COMPONENTS_md --> docs_SYSTEM_ARCHITECTURE_md
    docs_archive_COMPONENTS_md --> docs_SYSTEM_ARCHITECTURE_md
    docs_archive_COMPONENTS_md --> docs_DOCUMENTATION_GRAPH_md
    docs_archive_DATA_FLOW_md --> docs_SYSTEM_ARCHITECTURE_md
    docs_archive_DATA_FLOW_md --> docs_SYSTEM_ARCHITECTURE_md
    docs_archive_DATA_FLOW_md --> docs_DOCUMENTATION_GRAPH_md
    docs_archive_DIAGRAMS_md --> docs_SYSTEM_ARCHITECTURE_md
    docs_archive_DIAGRAMS_md --> docs_REPOSITORY_STRUCTURE_md
    docs_archive_ORGANIZATION_md --> docs_SYSTEM_ARCHITECTURE_md
    docs_archive_ORGANIZATION_md --> docs_REPOSITORY_STRUCTURE_md
    docs_archive_ORGANIZATION_md --> docs_SYSTEM_ARCHITECTURE_md
    docs_archive_ORGANIZATION_md --> docs_SYSTEM_ARCHITECTURE_md
    research_ARCHIVE_md --> research_README_md
    research_ARCHIVE_md --> research_DATA_GUIDE_md
    research_ARCHIVE_md --> research_REPORTS_md
    research_DATA_GUIDE_md --> data_DATA_DICTIONARY_md
    research_DATA_GUIDE_md --> research_README_md
    research_DATA_GUIDE_md --> data_DATA_DICTIONARY_md
    research_MASTER_INDEX_md --> research_README_md
    research_MASTER_INDEX_md --> research_QUICK_START_md
    research_MASTER_INDEX_md --> research_COMPLAINT_AMENDMENT_GUIDE_md
    research_MASTER_INDEX_md --> research_EVIDENCE_INDEX_md
    research_MASTER_INDEX_md --> research_REPORTS_md
    research_MASTER_INDEX_md --> research_DATA_GUIDE_md
    research_MASTER_INDEX_md --> research_ARCHIVE_md
    research_MASTER_INDEX_md --> research_ARCHIVE_md
    research_QUICK_START_md --> research_README_md
    research_QUICK_START_md --> research_COMPLAINT_AMENDMENT_GUIDE_md
    research_QUICK_START_md --> research_EVIDENCE_INDEX_md
    research_README_md --> research_REPORTS_md
    research_README_md --> research_REPORTS_md
    research_README_md --> research_ARCHIVE_md
    research_README_md --> research_REPORTS_md
    research_README_md --> research_DATA_GUIDE_md
    research_README_md --> data_DATA_CATALOG_md
    research_README_md --> research_REPORTS_md
    research_README_md --> data_DATA_CATALOG_md
    research_README_md --> data_DATA_DICTIONARY_md
    research_README_md --> research_DATA_GUIDE_md
    research_README_md --> docs_INDEX_md
    research_README_md --> docs_SYSTEM_ARCHITECTURE_md
    research_REPORTS_md --> research_reports_ALL_VIOLATIONS_AND_ANOMALIES_md
    research_REPORTS_md --> research_reports_COMPREHENSIVE_VIOLATIONS_REPORT_md
    research_REPORTS_md --> research_reports_ALL_ANOMALIES_SUMMARY_md
    research_REPORTS_md --> research_reports_COMPREHENSIVE_ANOMALIES_REPORT_md
    research_REPORTS_md --> research_reports_NEXUS_ANALYSIS_REPORT_md
    research_REPORTS_md --> research_reports_FINAL_NEXUS_FINDINGS_md
    research_REPORTS_md --> research_reports_COMPLETE_AUDIT_SUMMARY_md
    research_REPORTS_md --> research_reports_VIOLATION_AUDIT_COMPLETE_md
    research_REPORTS_md --> research_reports_RESEARCH_COMPLETION_SUMMARY_md
    research_REPORTS_md --> research_reports_FINAL_VIOLATION_SUMMARY_md
    research_REPORTS_md --> research_README_md
    research_REPORTS_md --> research_DATA_GUIDE_md
    research_investigations_README_md --> research_README_md
    research_investigations_README_md --> research_REPORTS_md
    research_investigations_README_md --> research_DATA_GUIDE_md
    research_license_searches_README_md --> research_license_searches_reports_INVESTIGATION_SUMMARY_md
    research_license_searches_README_md --> research_license_searches_reports_EXECUTIVE_SUMMARY_FOR_FILINGS_md
    research_license_searches_README_md --> research_license_searches_reports_COMPREHENSIVE_VIOLATIONS_REPORT_md
    research_license_searches_README_md --> research_license_searches_reports_ADMINISTRATIVE_FILING_CHECKLIST_md
    research_license_searches_README_md --> research_license_searches_reports_INVESTIGATION_SUMMARY_md
    research_license_searches_README_md --> research_README_md
    research_license_searches_README_md --> research_REPORTS_md
    research_license_searches_README_md --> research_DATA_GUIDE_md
    research_license_searches_README_md --> research_license_searches_reports_INVESTIGATION_SUMMARY_md
    research_license_searches_reports_COMPLETE_INVESTIGATION_PACKAGE_md --> research_license_searches_reports_EXECUTIVE_SUMMARY_FOR_FILINGS_md
    research_license_searches_reports_COMPLETE_INVESTIGATION_PACKAGE_md --> research_license_searches_archive_FINAL_INVESTIGATION_STATUS_md
    research_license_searches_reports_COMPLETE_INVESTIGATION_PACKAGE_md --> research_license_searches_archive_INVESTIGATION_COMPLETE_REPORT_md
    research_license_searches_reports_COMPLETE_INVESTIGATION_PACKAGE_md --> research_license_searches_reports_COMPREHENSIVE_VIOLATIONS_REPORT_md
    research_license_searches_reports_COMPLETE_INVESTIGATION_PACKAGE_md --> research_license_searches_reports_MASTER_INVESTIGATION_REPORT_md
    research_license_searches_reports_COMPLETE_INVESTIGATION_PACKAGE_md --> research_license_searches_reports_ADMINISTRATIVE_FILING_CHECKLIST_md
    research_license_searches_reports_INVESTIGATION_SUMMARY_md --> research_license_searches_reports_EXECUTIVE_SUMMARY_FOR_FILINGS_md
    research_license_searches_reports_INVESTIGATION_SUMMARY_md --> research_license_searches_reports_COMPREHENSIVE_VIOLATIONS_REPORT_md
    research_license_searches_reports_INVESTIGATION_SUMMARY_md --> research_license_searches_reports_MASTER_INVESTIGATION_REPORT_md
    research_license_searches_reports_INVESTIGATION_SUMMARY_md --> research_license_searches_README_md
    scripts_README_md --> docs_SYSTEM_ARCHITECTURE_md
    scripts_README_md --> docs_SYSTEM_ARCHITECTURE_md
    style INSTALLATION_md fill:#C8E6C9
    style QUICK_START_md fill:#C8E6C9
    style README_md fill:#C8E6C9
    style STATUS_md fill:#C8E6C9
    style docs_ARCHIVE_md fill:#B3E5FC
    style docs_DEPLOYMENT_md fill:#B3E5FC
    style docs_DOCUMENTATION_ARCHITECTURE_VERIFICATION_md fill:#B3E5FC
    style docs_DOCUMENTATION_GRAPH_md fill:#B3E5FC
    style docs_INDEX_md fill:#B3E5FC
    style docs_NAMING_CONVENTIONS_md fill:#B3E5FC
    style docs_REPOSITORY_STRUCTURE_md fill:#B3E5FC
    style docs_SYSTEM_ARCHITECTURE_md fill:#B3E5FC
    style docs_archive_COMPLETE_md fill:#B3E5FC
    style docs_archive_COMPLETE_INVESTIGATION_STATUS_md fill:#B3E5FC
    style docs_archive_COMPONENTS_md fill:#B3E5FC
    style docs_archive_DATA_FLOW_md fill:#B3E5FC
    style docs_archive_DIAGRAMS_md fill:#B3E5FC
    style docs_archive_FINAL_INVESTIGATION_REPORT_md fill:#B3E5FC
    style docs_archive_FINAL_STATUS_md fill:#B3E5FC
    style docs_archive_INVESTIGATION_COMPLETE_md fill:#B3E5FC
    style docs_archive_INVESTIGATION_COMPLETE_FINAL_md fill:#B3E5FC
    style docs_archive_INVESTIGATION_COMPLETE_SUMMARY_md fill:#B3E5FC
    style docs_archive_INVESTIGATION_FINAL_STATUS_md fill:#B3E5FC
    style docs_archive_INVESTIGATION_PACKAGE_COMPLETE_md fill:#B3E5FC
    style docs_archive_INVESTIGATION_STATUS_FINAL_md fill:#B3E5FC
    style docs_archive_MICROSERVICES_IMPLEMENTATION_COMPLETE_md fill:#B3E5FC
    style docs_archive_ORGANIZATION_md fill:#B3E5FC
    style docs_archive_REPOSITORY_REORGANIZATION_COMPLETE_md fill:#B3E5FC
    style data_ANCESTRY_md fill:#FFF9C4
    style data_DATA_CATALOG_md fill:#FFF9C4
    style data_DATA_DICTIONARY_md fill:#FFF9C4
    style data_GOVERNANCE_md fill:#FFF9C4
    style data_ONTOLOGY_md fill:#FFF9C4
    style data_README_md fill:#FFF9C4
    style research_ARCHIVE_md fill:#E1BEE7
    style research_COMPLAINT_AMENDMENT_GUIDE_md fill:#E1BEE7
    style research_DATA_GUIDE_md fill:#E1BEE7
    style research_EVIDENCE_INDEX_md fill:#E1BEE7
    style research_EXECUTIVE_SUMMARY_md fill:#E1BEE7
    style research_HANDOFF_DOCUMENT_md fill:#E1BEE7
    style research_MASTER_INDEX_md fill:#E1BEE7
    style research_QUICK_START_md fill:#E1BEE7
    style research_README_md fill:#E1BEE7
    style research_REPORTS_md fill:#E1BEE7
    style research_archive_COMPLETE_INVESTIGATION_SUMMARY_md fill:#E1BEE7
    style research_archive_COMPLETE_PACKAGE_SUMMARY_md fill:#E1BEE7
    style research_archive_EXECUTION_SUMMARY_md fill:#E1BEE7
    style research_archive_FINAL_DELIVERABLES_SUMMARY_md fill:#E1BEE7
    style research_archive_FINAL_STATUS_RECONCILIATION_md fill:#E1BEE7
    style research_archive_FINAL_VERIFICATION_REPORT_md fill:#E1BEE7
    style research_archive_FINDINGS_VALIDATION_REPORT_md fill:#E1BEE7
    style research_archive_INVESTIGATION_COMPLETE_GUIDE_md fill:#E1BEE7
    style research_archive_INVESTIGATION_STATISTICS_md fill:#E1BEE7
    style research_archive_INVESTIGATION_STATUS_COMPLETE_md fill:#E1BEE7
    style research_archive_MASTER_INVESTIGATION_STATUS_md fill:#E1BEE7
    style research_archive_MASTER_RESEARCH_COMPLETION_REPORT_md fill:#E1BEE7
    style research_archive_PROJECT_COMPLETE_md fill:#E1BEE7
    style research_archive_STATUS_FILES_ARCHIVE_md fill:#E1BEE7
    style research_archive_VALIDATION_REPORT_md fill:#E1BEE7
    style research_archive_VIRGINIA_EXTRACTION_COMPLETE_SUMMARY_md fill:#E1BEE7
    style research_archive_VIRGINIA_EXTRACTION_FINAL_STATUS_md fill:#E1BEE7
    style research_archive_VIRGINIA_EXTRACTION_STATUS_md fill:#E1BEE7
    style research_archive_VIRGINIA_EXTRACTION_SUMMARY_md fill:#E1BEE7
    style research_browser_automation_DATABASE_SEARCH_FRAMEWORK_md fill:#E1BEE7
    style research_browser_automation_README_md fill:#E1BEE7
    style research_investigations_README_md fill:#E1BEE7
    style research_investigations_hyland_upl_evidence_md fill:#E1BEE7
    style research_investigations_kettler_operational_locations_md fill:#E1BEE7
    style research_investigations_lariat_affiliated_companies_investigation_md fill:#E1BEE7
    style research_investigations_lariat_affiliated_companies_summary_md fill:#E1BEE7
    style research_investigations_lariat_broker_for_rent_analysis_md fill:#E1BEE7
    style research_investigations_lariat_companies_findings_md fill:#E1BEE7
    style research_investigations_lariat_companies_search_md fill:#E1BEE7
    style research_investigations_lariat_vs_kettler_licensing_strategy_md fill:#E1BEE7
    style research_investigations_method_comparison_md fill:#E1BEE7
    style research_investigations_moore_kristen_jones_investigation_md fill:#E1BEE7
    style research_investigations_remaining_legal_violations_md fill:#E1BEE7
    style research_investigations_virginia_40_licenses_finding_md fill:#E1BEE7
    style research_investigations_virginia_companies_found_md fill:#E1BEE7
    style research_license_searches_100_PERCENT_COVERAGE_CONFIRMED_md fill:#E1BEE7
    style research_license_searches_KEY_FINDINGS_DC_md fill:#E1BEE7
    style research_license_searches_LEAH_DOUTHIT_LIDDY_BISANZ_SEARCH_PLAN_md fill:#E1BEE7
    style research_license_searches_LICENSE_SEARCHES_COMPLETE_md fill:#E1BEE7
    style research_license_searches_LICENSE_SEARCHES_FINAL_COMPLETE_md fill:#E1BEE7
    style research_license_searches_README_md fill:#E1BEE7
    style research_license_searches_READY_FOR_FILINGS_md fill:#E1BEE7
    style research_license_searches_REORGANIZATION_AND_PROGRESS_md fill:#E1BEE7
    style research_license_searches_REORGANIZATION_COMPLETE_md fill:#E1BEE7
    style research_license_searches_ROBERT_KETTLER_SUMMARY_md fill:#E1BEE7
    style research_license_searches_SEAN_CURTIN_BAR_LICENSE_SEARCH_md fill:#E1BEE7
    style research_license_searches_UNLICENSED_OPERATIONS_REPORT_md fill:#E1BEE7
    style research_license_searches_archive_BATCH_SEARCH_PROGRESS_md fill:#E1BEE7
    style research_license_searches_archive_CURRENT_PROGRESS_UPDATE_md fill:#E1BEE7
    style research_license_searches_archive_CURRENT_SEARCH_STATUS_md fill:#E1BEE7
    style research_license_searches_archive_CURRENT_STATUS_md fill:#E1BEE7
    style research_license_searches_archive_CURRENT_STATUS_SUMMARY_md fill:#E1BEE7
    style research_license_searches_archive_FINAL_BATCH_PROGRESS_md fill:#E1BEE7
    style research_license_searches_archive_FINAL_COMPLETION_SUMMARY_md fill:#E1BEE7
    style research_license_searches_archive_FINAL_INVESTIGATION_STATUS_md fill:#E1BEE7
    style research_license_searches_archive_FINAL_INVESTIGATION_SUMMARY_md fill:#E1BEE7
    style research_license_searches_archive_FINAL_STATUS_REPORT_md fill:#E1BEE7
    style research_license_searches_archive_INVESTIGATION_COMPLETE_REPORT_md fill:#E1BEE7
    style research_license_searches_archive_INVESTIGATION_COMPLETE_SUMMARY_md fill:#E1BEE7
    style research_license_searches_archive_INVESTIGATION_STATUS_UPDATE_md fill:#E1BEE7
    style research_license_searches_archive_LATEST_FINDINGS_UPDATE_md fill:#E1BEE7
    style research_license_searches_archive_PROGRESS_SUMMARY_FINAL_md fill:#E1BEE7
    style research_license_searches_archive_PROGRESS_UPDATE_md fill:#E1BEE7
    style research_license_searches_archive_REMAINING_WORK_SUMMARY_md fill:#E1BEE7
    style research_license_searches_archive_SEARCH_PROGRESS_UPDATE_md fill:#E1BEE7
    style research_license_searches_archive_completion_status_ALL_FINDINGS_SUMMARY_md fill:#E1BEE7
    style research_license_searches_archive_completion_status_AUTOMATION_READY_md fill:#E1BEE7
    style research_license_searches_archive_completion_status_CAITLIN_SKIDMORE_MULTI_STATE_md fill:#E1BEE7
    style research_license_searches_archive_completion_status_COMPLETE_OPERATIONAL_STATES_SEARCH_md fill:#E1BEE7
    style research_license_searches_archive_completion_status_COMPREHENSIVE_FINAL_STATUS_md fill:#E1BEE7
    style research_license_searches_archive_completion_status_COMPREHENSIVE_PROGRESS_md fill:#E1BEE7
    style research_license_searches_archive_completion_status_CONSOLIDATED_FINDINGS_SUMMARY_md fill:#E1BEE7
    style research_license_searches_archive_completion_status_CORE_15_EMPLOYEES_LIST_md fill:#E1BEE7
    style research_license_searches_archive_completion_status_CRITICAL_PATTERN_UPDATE_md fill:#E1BEE7
    style research_license_searches_archive_completion_status_DATA_VERIFICATION_FINAL_md fill:#E1BEE7
    style research_license_searches_archive_completion_status_DMV_COMPLETENESS_VERIFICATION_md fill:#E1BEE7
    style research_license_searches_archive_completion_status_DMV_FINAL_STATUS_md fill:#E1BEE7
    style research_license_searches_archive_completion_status_FINAL_COMPREHENSIVE_STATUS_md fill:#E1BEE7
    style research_license_searches_archive_completion_status_FINAL_REORGANIZATION_SUMMARY_md fill:#E1BEE7
    style research_license_searches_archive_completion_status_FINAL_VALIDATION_SUMMARY_md fill:#E1BEE7
    style research_license_searches_archive_completion_status_ISSUES_ENCOUNTERED_md fill:#E1BEE7
    style research_license_searches_archive_completion_status_KEY_FINDINGS_COMPREHENSIVE_md fill:#E1BEE7
    style research_license_searches_archive_completion_status_LATEST_BATCH_RESULTS_md fill:#E1BEE7
    style research_license_searches_archive_completion_status_LATEST_FINDINGS_md fill:#E1BEE7
    style research_license_searches_archive_completion_status_NEXT_STEPS_md fill:#E1BEE7
    style research_license_searches_archive_completion_status_NJ_NY_COMPLETE_SUMMARY_md fill:#E1BEE7
    style research_license_searches_archive_completion_status_SEARCH_COMPLETION_STATUS_md fill:#E1BEE7
    style research_license_searches_archive_completion_status_SEARCH_COMPLETION_SUMMARY_md fill:#E1BEE7
    style research_license_searches_archive_completion_status_SUMMARY_AND_STATUS_md fill:#E1BEE7
    style research_license_searches_archive_completion_status_THOMAS_BISANZ_SEARCH_COMPLETE_md fill:#E1BEE7
    style research_license_searches_archive_completion_status_URLS_AND_PROGRESS_md fill:#E1BEE7
    style research_license_searches_archive_completion_status_VALIDATION_REPORT_md fill:#E1BEE7
    style research_license_searches_archive_completion_status_VERIFICATION_COMPLETE_md fill:#E1BEE7
    style research_license_searches_data_connecticut_BROWSER_AUTOMATION_EXECUTED_md fill:#E1BEE7
    style research_license_searches_data_connecticut_CONNECTICUT_SEARCH_STATUS_md fill:#E1BEE7
    style research_license_searches_data_dc_DC_SEARCH_COMPLETE_md fill:#E1BEE7
    style research_license_searches_data_maryland_ADDITIONAL_MARYLAND_SEARCHES_md fill:#E1BEE7
    style research_license_searches_data_maryland_CAPTCHA_BYPASS_OPTIONS_md fill:#E1BEE7
    style research_license_searches_data_maryland_CAPTCHA_REQUIRED_md fill:#E1BEE7
    style research_license_searches_data_maryland_CAPTCHA_SERVICE_SETUP_md fill:#E1BEE7
    style research_license_searches_data_maryland_IMPLEMENTATION_STATUS_md fill:#E1BEE7
    style research_license_searches_data_maryland_MANUAL_CAPTCHA_INSTRUCTIONS_md fill:#E1BEE7
    style research_license_searches_data_maryland_MANUAL_SEARCH_CHECKLIST_md fill:#E1BEE7
    style research_license_searches_data_maryland_MARYLAND_CAPTCHA_SOLUTION_SUMMARY_md fill:#E1BEE7
    style research_license_searches_data_maryland_MARYLAND_FINDINGS_SUMMARY_md fill:#E1BEE7
    style research_license_searches_data_maryland_MARYLAND_LICENSED_EMPLOYEES_UPDATE_md fill:#E1BEE7
    style research_license_searches_data_maryland_MARYLAND_PROGRESS_md fill:#E1BEE7
    style research_license_searches_data_maryland_MARYLAND_SEARCH_STATUS_md fill:#E1BEE7
    style research_license_searches_data_maryland_MARYLAND_SEARCH_STRATEGY_md fill:#E1BEE7
    style research_license_searches_data_maryland_SETUP_CAPTCHA_SERVICE_md fill:#E1BEE7
    style research_license_searches_reports_ACTION_PLAN_md fill:#E1BEE7
    style research_license_searches_reports_ADMINISTRATIVE_FILING_CHECKLIST_md fill:#E1BEE7
    style research_license_searches_reports_COMPLETE_INVESTIGATION_PACKAGE_md fill:#E1BEE7
    style research_license_searches_reports_COMPREHENSIVE_VIOLATIONS_REPORT_md fill:#E1BEE7
    style research_license_searches_reports_EXECUTIVE_SUMMARY_FOR_FILINGS_md fill:#E1BEE7
    style research_license_searches_reports_INVESTIGATION_SUMMARY_md fill:#E1BEE7
    style research_license_searches_reports_MASTER_INVESTIGATION_REPORT_md fill:#E1BEE7
    style research_license_searches_reports_QUICK_REFERENCE_md fill:#E1BEE7
    style research_reports_ALL_ANOMALIES_SUMMARY_md fill:#E1BEE7
    style research_reports_ALL_VIOLATIONS_AND_ANOMALIES_md fill:#E1BEE7
    style research_reports_COMPLETE_AUDIT_SUMMARY_md fill:#E1BEE7
    style research_reports_COMPREHENSIVE_ANOMALIES_REPORT_md fill:#E1BEE7
    style research_reports_COMPREHENSIVE_VIOLATIONS_REPORT_md fill:#E1BEE7
    style research_reports_FINAL_NEXUS_FINDINGS_md fill:#E1BEE7
    style research_reports_FINAL_VIOLATION_SUMMARY_md fill:#E1BEE7
    style research_reports_NEXUS_ANALYSIS_REPORT_md fill:#E1BEE7
    style research_reports_RESEARCH_COMPLETION_SUMMARY_md fill:#E1BEE7
    style research_reports_VIOLATION_AUDIT_COMPLETE_md fill:#E1BEE7
    style research_reports_validation_report_md fill:#E1BEE7
    style research_va_dpor_complaint_evidence_exhibits_compilation_md fill:#E1BEE7
    style docs_SYSTEM_ANALYST_GUIDE_md fill:#F8BBD0
    style CODE_FIXES_SUMMARY_md fill:#D1C4E9
    style INSTALL_PYTHON_3_14_md fill:#D1C4E9
    style INVESTIGATION_READY_md fill:#D1C4E9
    style SUMMARY_md fill:#D1C4E9
    style scripts_README_md fill:#D1C4E9
    style scripts_automation_BROWSER_AUTOMATION_TROUBLESHOOTING_md fill:#D1C4E9
    style scripts_automation_EXPANSION_COMPLETE_md fill:#D1C4E9
    style scripts_automation_README_md fill:#D1C4E9
    style scripts_automation_README_DEVTOOLS_md fill:#D1C4E9
    style scripts_automation_UNIVERSAL_SCRAPER_GUIDE_md fill:#D1C4E9
    style scripts_automation_devtools_scraping_guide_md fill:#D1C4E9
```
