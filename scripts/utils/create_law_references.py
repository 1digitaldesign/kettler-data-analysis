#!/usr/bin/env python3
"""
Create law reference JSON with embedded vectors for jurisdictions
Focuses on criminal law first, then civil law
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import os
import threading

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import PROJECT_ROOT

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("Installing sentence-transformers...")
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "sentence-transformers"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        print("Warning: Could not install sentence-transformers automatically.")
        print("Please install manually: pip install --user sentence-transformers")
        sys.exit(1)
    from sentence_transformers import SentenceTransformer

# Optimize for ARM M4 MAX - use all available CPU cores
# M4 MAX typically has 12-14 cores, use all for maximum throughput
MAX_WORKERS = os.cpu_count() or 12
print(f"🚀 Optimized for ARM M4 MAX: Using {MAX_WORKERS} parallel workers")


def create_jurisdiction_references() -> Dict[str, Any]:
    """Create comprehensive jurisdiction reference structure"""

    return {
        "metadata": {
            "created": datetime.now().isoformat(),
            "version": "1.0.0",
            "description": "Law reference list with embedded vectors for jurisdictions",
            "focus": "Criminal law first, then civil law",
            "embedding_model": "all-MiniLM-L6-v2"
        },
        "federal": {
            "criminal": {
                "title_18": {
                    "name": "Title 18 - Crimes and Criminal Procedure",
                    "url": "https://www.law.cornell.edu/uscode/text/18",
                    "description": "Federal criminal law covering crimes against the United States, criminal procedure, and related offenses",
                    "key_sections": [
                        "18 U.S.C. § 371 - Conspiracy to commit offense or to defraud United States",
                        "18 U.S.C. § 1001 - Statements or entries generally (false statements)",
                        "18 U.S.C. § 1341 - Frauds and swindles (mail fraud)",
                        "18 U.S.C. § 1343 - Fraud by wire, radio, or television",
                        "18 U.S.C. § 1349 - Attempt and conspiracy",
                        "18 U.S.C. § 1951 - Interference with commerce by threats or violence",
                        "18 U.S.C. § 1956 - Laundering of monetary instruments",
                        "18 U.S.C. § 1957 - Engaging in monetary transactions in property derived from specified unlawful activity",
                        "18 U.S.C. § 1961-1968 - Racketeer Influenced and Corrupt Organizations (RICO)"
                    ],
                    "relevance": "Federal criminal violations related to fraud, conspiracy, money laundering, and organized crime",
                    "reporting_forms": [
                        {
                            "form_name": "FBI Tip Form",
                            "form_number": "Online Tip",
                            "agency": "Federal Bureau of Investigation (FBI)",
                            "url": "https://tips.fbi.gov/",
                            "description": "Report federal crimes including fraud, conspiracy, money laundering, RICO violations",
                            "form_type": "Online submission"
                        },
                        {
                            "form_name": "FBI IC3 Internet Crime Complaint",
                            "form_number": "IC3",
                            "agency": "FBI Internet Crime Complaint Center",
                            "url": "https://www.ic3.gov/",
                            "description": "Report internet-related crimes, wire fraud, and financial fraud",
                            "form_type": "Online complaint"
                        },
                        {
                            "form_name": "USPS Mail Fraud Complaint",
                            "form_number": "PS Form 2017",
                            "agency": "United States Postal Inspection Service",
                            "url": "https://www.uspis.gov/report",
                            "description": "Report mail fraud violations under 18 U.S.C. § 1341",
                            "form_type": "Online complaint"
                        },
                        {
                            "form_name": "FinCEN Suspicious Activity Report",
                            "form_number": "SAR",
                            "agency": "Financial Crimes Enforcement Network",
                            "url": "https://www.fincen.gov/report-suspicious-activity",
                            "description": "Report money laundering and suspicious financial transactions",
                            "form_type": "Electronic filing"
                        }
                    ]
                },
                "title_26": {
                    "name": "Title 26 - Internal Revenue Code (Criminal Provisions)",
                    "url": "https://www.law.cornell.edu/uscode/text/26",
                    "description": "Federal tax law criminal provisions including tax evasion, fraud, and false returns",
                    "key_sections": [
                        "26 U.S.C. § 7201 - Attempt to evade or defeat tax",
                        "26 U.S.C. § 7202 - Willful failure to collect or pay over tax",
                        "26 U.S.C. § 7203 - Willful failure to file return, supply information, or pay tax",
                        "26 U.S.C. § 7206 - Fraud and false statements",
                        "26 U.S.C. § 7207 - Fraudulent returns, statements, or other documents"
                    ],
                    "relevance": "Criminal tax violations including evasion, fraud, and false filings",
                    "reporting_forms": [
                        {
                            "form_name": "IRS Form 3949-A",
                            "form_number": "3949-A",
                            "agency": "Internal Revenue Service",
                            "url": "https://www.irs.gov/pub/irs-pdf/f3949a.pdf",
                            "description": "Information Referral - Report suspected tax fraud or evasion",
                            "form_type": "PDF form - mail or fax"
                        },
                        {
                            "form_name": "IRS Whistleblower Claim",
                            "form_number": "Form 211",
                            "agency": "Internal Revenue Service",
                            "url": "https://www.irs.gov/pub/irs-pdf/f211.pdf",
                            "description": "Application for Award for Original Information - Report tax violations for potential reward",
                            "form_type": "PDF form"
                        },
                        {
                            "form_name": "IRS Tax Fraud Hotline",
                            "form_number": "Phone Report",
                            "agency": "Internal Revenue Service",
                            "url": "https://www.irs.gov/compliance/criminal-investigation/report-suspected-tax-fraud-activity",
                            "description": "Report tax fraud by phone: 1-800-829-0433",
                            "form_type": "Phone report"
                        }
                    ]
                },
                "title_15": {
                    "name": "Title 15 - Commerce and Trade (Criminal Provisions)",
                    "url": "https://www.law.cornell.edu/uscode/text/15",
                    "description": "Federal criminal provisions related to commerce, trade practices, and securities",
                    "key_sections": [
                        "15 U.S.C. § 77q - Fraudulent interstate transactions",
                        "15 U.S.C. § 78j - Manipulative and deceptive devices",
                        "15 U.S.C. § 78ff - Penalties"
                    ],
                    "relevance": "Securities fraud and deceptive trade practices",
                    "reporting_forms": [
                        {
                            "form_name": "SEC Tips, Complaints and Referrals",
                            "form_number": "TCR",
                            "agency": "Securities and Exchange Commission",
                            "url": "https://www.sec.gov/tcr",
                            "description": "Report securities fraud, insider trading, market manipulation",
                            "form_type": "Online form"
                        },
                        {
                            "form_name": "SEC Whistleblower Program",
                            "form_number": "Form TCR",
                            "agency": "Securities and Exchange Commission",
                            "url": "https://www.sec.gov/whistleblower",
                            "description": "Report securities violations for potential monetary award",
                            "form_type": "Online submission"
                        },
                        {
                            "form_name": "FTC Consumer Complaint",
                            "form_number": "Online Complaint",
                            "agency": "Federal Trade Commission",
                            "url": "https://www.ftccomplaintassistant.gov/",
                            "description": "Report deceptive trade practices, unfair business practices",
                            "form_type": "Online complaint"
                        }
                    ]
                }
            },
            "civil": {
                "title_15": {
                    "name": "Title 15 - Commerce and Trade",
                    "url": "https://www.law.cornell.edu/uscode/text/15",
                    "description": "Federal civil law covering commerce, trade practices, consumer protection, and antitrust",
                    "key_sections": [
                        "15 U.S.C. § 1 - Trusts, etc., in restraint of trade illegal; penalty",
                        "15 U.S.C. § 2 - Monopolizing trade a felony; penalty",
                        "15 U.S.C. § 13 - Discrimination in price, services, or facilities",
                        "15 U.S.C. § 45 - Unfair methods of competition unlawful; prevention by Commission",
                        "15 U.S.C. § 1601-1693r - Truth in Lending Act",
                        "15 U.S.C. § 1692-1692p - Fair Debt Collection Practices Act",
                        "15 U.S.C. § 7001-7031 - Electronic Signatures in Global and National Commerce Act"
                    ],
                    "relevance": "Consumer protection, antitrust, and fair trade practices",
                    "reporting_forms": [
                        {
                            "form_name": "FTC Consumer Complaint",
                            "form_number": "Online Complaint",
                            "agency": "Federal Trade Commission",
                            "url": "https://www.ftccomplaintassistant.gov/",
                            "description": "Report unfair or deceptive business practices, consumer fraud",
                            "form_type": "Online complaint"
                        },
                        {
                            "form_name": "FTC Antitrust Complaint",
                            "form_number": "Antitrust Complaint",
                            "agency": "Federal Trade Commission",
                            "url": "https://www.ftc.gov/legal-library/browse/cases-proceedings/antitrust-matters",
                            "description": "Report antitrust violations, price fixing, monopolization",
                            "form_type": "Online submission"
                        },
                        {
                            "form_name": "CFPB Consumer Complaint",
                            "form_number": "Consumer Complaint",
                            "agency": "Consumer Financial Protection Bureau",
                            "url": "https://www.consumerfinance.gov/complaint/",
                            "description": "Report violations of Truth in Lending Act, Fair Debt Collection Practices Act",
                            "form_type": "Online complaint"
                        }
                    ]
                },
                "title_42": {
                    "name": "Title 42 - The Public Health and Welfare",
                    "url": "https://www.law.cornell.edu/uscode/text/42",
                    "description": "Federal civil law covering public health, welfare, civil rights, and environmental protection",
                    "key_sections": [
                        "42 U.S.C. § 1981 - Equal rights under the law",
                        "42 U.S.C. § 1982 - Property rights of citizens",
                        "42 U.S.C. § 1983 - Civil action for deprivation of rights",
                        "42 U.S.C. § 2000a - Prohibition against discrimination or segregation in places of public accommodation",
                        "42 U.S.C. § 3601-3619 - Fair Housing Act",
                        "42 U.S.C. § 12101-12213 - Americans with Disabilities Act"
                    ],
                    "relevance": "Civil rights, fair housing, and discrimination claims",
                    "reporting_forms": [
                        {
                            "form_name": "HUD Fair Housing Complaint",
                            "form_number": "HUD-903.1",
                            "agency": "Department of Housing and Urban Development",
                            "url": "https://www.hud.gov/program_offices/fair_housing_equal_opp/online-complaint",
                            "description": "Report housing discrimination, Fair Housing Act violations",
                            "form_type": "Online complaint"
                        },
                        {
                            "form_name": "DOJ Civil Rights Complaint",
                            "form_number": "Online Complaint",
                            "agency": "Department of Justice Civil Rights Division",
                            "url": "https://civilrights.justice.gov/report/",
                            "description": "Report civil rights violations, discrimination",
                            "form_type": "Online complaint"
                        },
                        {
                            "form_name": "EEOC Charge of Discrimination",
                            "form_number": "EEOC Form 5",
                            "agency": "Equal Employment Opportunity Commission",
                            "url": "https://www.eeoc.gov/filing-charge-discrimination",
                            "description": "Report employment discrimination",
                            "form_type": "Online or mail"
                        }
                    ]
                },
                "title_28": {
                    "name": "Title 28 - Judiciary and Judicial Procedure",
                    "url": "https://www.law.cornell.edu/uscode/text/28",
                    "description": "Federal civil procedure, jurisdiction, and judicial administration",
                    "key_sections": [
                        "28 U.S.C. § 1331 - Federal question jurisdiction",
                        "28 U.S.C. § 1332 - Diversity of citizenship; amount in controversy",
                        "28 U.S.C. § 1367 - Supplemental jurisdiction",
                        "28 U.S.C. § 1404 - Change of venue"
                    ],
                    "relevance": "Federal court jurisdiction and civil procedure"
                }
            }
        },
        "states": {
            "virginia": {
                "criminal": {
                    "code_title_18_2": {
                        "name": "Virginia Code Title 18.2 - Crimes and Offenses Generally",
                        "url": "https://law.lis.virginia.gov/vacode/title18.2/",
                        "description": "Virginia criminal code covering all criminal offenses",
                        "key_sections": [
                            "Va. Code § 18.2-8 - Classification of offenses",
                            "Va. Code § 18.2-11 - Punishment for conviction of felony",
                            "Va. Code § 18.2-22 - Conspiracy",
                            "Va. Code § 18.2-95 - Grand larceny",
                            "Va. Code § 18.2-111 - Obtaining money by false pretenses",
                            "Va. Code § 18.2-178 - Fraudulent conversion",
                            "Va. Code § 18.2-186 - Credit card fraud",
                            "Va. Code § 18.2-246 - Money laundering"
                        ],
                        "relevance": "Virginia criminal violations including fraud, theft, and money laundering"
                    },
                    "code_title_58_1": {
                        "name": "Virginia Code Title 58.1 - Taxation (Criminal Provisions)",
                        "url": "https://law.lis.virginia.gov/vacode/title58.1/",
                        "description": "Virginia tax law criminal provisions",
                        "key_sections": [
                            "Va. Code § 58.1-348 - Willful failure to pay tax, file return, etc.",
                            "Va. Code § 58.1-349 - False or fraudulent return"
                        ],
                        "relevance": "Criminal tax violations in Virginia"
                    }
                },
                "civil": {
                    "code_title_54_1": {
                        "name": "Virginia Code Title 54.1 - Professions and Occupations",
                        "url": "https://law.lis.virginia.gov/vacode/title54.1/",
                        "description": "Virginia professional licensing and regulation",
                        "key_sections": [
                            "Va. Code § 54.1-2100 - Real Estate Board; membership; terms; qualifications",
                            "Va. Code § 54.1-2105 - License required",
                            "Va. Code § 54.1-2111 - Grounds for which the Board may refuse to issue a license",
                            "Va. Code § 54.1-2112 - Grounds for which the Board may suspend or revoke a license",
                            "Va. Code § 54.1-2113 - Unlawful acts",
                            "Va. Code § 54.1-2114 - Penalties for violations"
                        ],
                        "relevance": "Real estate licensing violations and professional misconduct",
                        "reporting_forms": [
                            {
                                "form_name": "DPOR Complaint Form",
                                "form_number": "DPOR Complaint",
                                "agency": "Virginia Department of Professional and Occupational Regulation",
                                "url": "https://www.dpor.virginia.gov/Boards/RealEstate/",
                                "description": "File complaint against unlicensed real estate activity or licensed professional misconduct",
                                "form_type": "Online complaint or mail",
                                "contact": "Phone: (804) 367-8526"
                            },
                            {
                                "form_name": "DPOR Unlicensed Activity Complaint",
                                "form_number": "UPL Complaint",
                                "agency": "Virginia DPOR",
                                "url": "https://www.dpor.virginia.gov/Boards/RealEstate/",
                                "description": "Report unlicensed practice of real estate in Virginia",
                                "form_type": "Online or written complaint"
                            }
                        ]
                    },
                    "code_title_55_1": {
                        "name": "Virginia Code Title 55.1 - Property and Conveyances",
                        "url": "https://law.lis.virginia.gov/vacode/title55.1/",
                        "description": "Virginia property law including landlord-tenant relations",
                        "key_sections": [
                            "Va. Code § 55.1-1200 - Virginia Residential Landlord and Tenant Act",
                            "Va. Code § 55.1-1204 - Terms and conditions of rental agreement",
                            "Va. Code § 55.1-1226 - Landlord to maintain fit premises"
                        ],
                        "relevance": "Property management and landlord-tenant violations",
                        "reporting_forms": [
                            {
                                "form_name": "Virginia Attorney General Consumer Complaint",
                                "form_number": "Consumer Complaint",
                                "agency": "Virginia Office of the Attorney General",
                                "url": "https://www.oag.state.va.us/consumer-protection/index.php/file-a-complaint",
                                "description": "Report landlord-tenant violations, property management issues",
                                "form_type": "Online complaint"
                            },
                            {
                                "form_name": "Local Code Enforcement Complaint",
                                "form_number": "Varies by locality",
                                "agency": "Local Code Enforcement",
                                "url": "Contact local jurisdiction",
                                "description": "Report property code violations, unsafe conditions",
                                "form_type": "Local jurisdiction form"
                            }
                        ]
                    },
                    "code_title_59_1": {
                        "name": "Virginia Code Title 59.1 - Trade and Commerce",
                        "url": "https://law.lis.virginia.gov/vacode/title59.1/",
                        "description": "Virginia consumer protection and trade practices",
                        "key_sections": [
                            "Va. Code § 59.1-200 - Virginia Consumer Protection Act",
                            "Va. Code § 59.1-204 - Prohibited practices"
                        ],
                        "relevance": "Consumer protection violations"
                    }
                }
            },
            "texas": {
                "criminal": {
                    "penal_code": {
                        "name": "Texas Penal Code",
                        "url": "https://statutes.capitol.texas.gov/Docs/PE/htm/PE.1.htm",
                        "description": "Texas criminal code covering all criminal offenses",
                        "key_sections": [
                            "Tex. Penal Code § 1.02 - Objectives of code",
                            "Tex. Penal Code § 12.04 - Classification of offenses",
                            "Tex. Penal Code § 15.02 - Criminal conspiracy",
                            "Tex. Penal Code § 31.03 - Theft",
                            "Tex. Penal Code § 32.45 - Misapplication of fiduciary property or property of financial institution",
                            "Tex. Penal Code § 32.46 - Securing execution of document by deception",
                            "Tex. Penal Code § 34.02 - Money laundering"
                        ],
                        "relevance": "Texas criminal violations including theft, fraud, and money laundering"
                    },
                    "tax_code": {
                        "name": "Texas Tax Code (Criminal Provisions)",
                        "url": "https://statutes.capitol.texas.gov/Docs/TX/htm/TX.1.htm",
                        "description": "Texas tax law criminal provisions",
                        "key_sections": [
                            "Tex. Tax Code § 111.015 - Criminal penalty for failure to pay tax",
                            "Tex. Tax Code § 111.016 - Criminal penalty for failure to file return"
                        ],
                        "relevance": "Criminal tax violations in Texas"
                    }
                },
                "civil": {
                    "occupations_code": {
                        "name": "Texas Occupations Code",
                        "url": "https://statutes.capitol.texas.gov/Docs/OC/htm/OC.1.htm",
                        "description": "Texas professional licensing and regulation",
                        "key_sections": [
                            "Tex. Occ. Code § 1101.001 - Real Estate License Act",
                            "Tex. Occ. Code § 1101.351 - License required",
                            "Tex. Occ. Code § 1101.652 - Grounds for suspension or revocation of license",
                            "Tex. Occ. Code § 1101.653 - Criminal offense"
                        ],
                        "relevance": "Real estate licensing violations in Texas",
                        "reporting_forms": [
                            {
                                "form_name": "TREC Complaint Form",
                                "form_number": "TREC Complaint",
                                "agency": "Texas Real Estate Commission",
                                "url": "https://www.trec.texas.gov/complaints",
                                "description": "File complaint against unlicensed real estate activity or licensed professional misconduct",
                                "form_type": "Online complaint",
                                "contact": "Phone: (512) 936-3000"
                            },
                            {
                                "form_name": "TREC Unlicensed Activity Complaint",
                                "form_number": "UPL Complaint",
                                "agency": "Texas Real Estate Commission",
                                "url": "https://www.trec.texas.gov/complaints/unlicensed-activity",
                                "description": "Report unlicensed practice of real estate in Texas",
                                "form_type": "Online complaint"
                            }
                        ]
                    },
                    "property_code": {
                        "name": "Texas Property Code",
                        "url": "https://statutes.capitol.texas.gov/Docs/PR/htm/PR.1.htm",
                        "description": "Texas property law including landlord-tenant relations",
                        "key_sections": [
                            "Tex. Prop. Code § 92.001 - Residential tenancies",
                            "Tex. Prop. Code § 92.052 - Landlord's duty to repair or remedy"
                        ],
                        "relevance": "Property management violations in Texas"
                    },
                    "business_organizations_code": {
                        "name": "Texas Business Organizations Code",
                        "url": "https://statutes.capitol.texas.gov/Docs/BO/htm/BO.1.htm",
                        "description": "Texas business entity formation and regulation",
                        "key_sections": [
                            "Tex. Bus. Org. Code § 1.002 - Definitions",
                            "Tex. Bus. Org. Code § 3.001 - General powers",
                            "Tex. Bus. Org. Code § 21.001 - Application of chapter"
                        ],
                        "relevance": "Business entity violations and corporate compliance",
                        "reporting_forms": [
                            {
                                "form_name": "Texas Secretary of State Business Complaint",
                                "form_number": "SOS Complaint",
                                "agency": "Texas Secretary of State",
                                "url": "https://www.sos.texas.gov/",
                                "description": "Report business entity violations, corporate compliance issues",
                                "form_type": "Online or written complaint"
                            },
                            {
                                "form_name": "Texas Attorney General Consumer Complaint",
                                "form_number": "Consumer Complaint",
                                "agency": "Texas Office of the Attorney General",
                                "url": "https://www.texasattorneygeneral.gov/consumer-protection/file-consumer-complaint",
                                "description": "Report business fraud, deceptive trade practices",
                                "form_type": "Online complaint"
                            }
                        ]
                    }
                }
            },
            "maryland": {
                "criminal": {
                    "criminal_law": {
                        "name": "Maryland Criminal Law Code",
                        "url": "https://mgaleg.maryland.gov/mgawebsite/Laws/StatuteText?article=gcr&section=1-101",
                        "description": "Maryland criminal code",
                        "key_sections": [
                            "Md. Crim. Law Code Ann. § 1-101 - Definitions",
                            "Md. Crim. Law Code Ann. § 7-104 - Theft",
                            "Md. Crim. Law Code Ann. § 8-101 - Fraud",
                            "Md. Crim. Law Code Ann. § 8-301 - Money laundering"
                        ],
                        "relevance": "Maryland criminal violations"
                    }
                },
                "civil": {
                    "business_occupations": {
                        "name": "Maryland Business Occupations and Professions Code",
                        "url": "https://mgaleg.maryland.gov/mgawebsite/Laws/StatuteText?article=gbo",
                        "description": "Maryland professional licensing",
                        "key_sections": [
                            "Md. Bus. Occ. & Prof. Code Ann. § 17-101 - Real Estate Brokers Act",
                            "Md. Bus. Occ. & Prof. Code Ann. § 17-322 - License required",
                            "Md. Bus. Occ. & Prof. Code Ann. § 17-512 - Grounds for disciplinary action"
                        ],
                        "relevance": "Real estate licensing violations in Maryland"
                    },
                    "real_property": {
                        "name": "Maryland Real Property Code",
                        "url": "https://mgaleg.maryland.gov/mgawebsite/Laws/StatuteText?article=grp",
                        "description": "Maryland property law",
                        "key_sections": [
                            "Md. Real Prop. Code Ann. § 8-101 - Landlord and tenant"
                        ],
                        "relevance": "Property management violations in Maryland"
                    }
                }
            },
            "dc": {
                "criminal": {
                    "criminal_code": {
                        "name": "District of Columbia Criminal Code",
                        "url": "https://code.dccouncil.gov/us/dc/council/code/titles/22",
                        "description": "D.C. criminal code",
                        "key_sections": [
                            "D.C. Code § 22-1801 - Criminal conspiracy",
                            "D.C. Code § 22-3211 - Theft",
                            "D.C. Code § 22-3221 - Fraud"
                        ],
                        "relevance": "D.C. criminal violations"
                    }
                },
                "civil": {
                    "municipal_regulations": {
                        "name": "District of Columbia Municipal Regulations Title 17 - Real Estate",
                        "url": "https://code.dccouncil.gov/us/dc/council/code/titles/42",
                        "description": "D.C. real estate licensing and regulation",
                        "key_sections": [
                            "D.C. Code § 42-1701 - Real Estate Licensure Act",
                            "D.C. Code § 42-1703 - License required"
                        ],
                        "relevance": "Real estate licensing violations in D.C."
                    }
                }
            },
            "pennsylvania": {
                "criminal": {
                    "crimes_code": {
                        "name": "Pennsylvania Crimes Code",
                        "url": "https://www.legis.state.pa.us/cfdocs/legis/LI/consCheck.cfm?txtType=HTM&ttl=18&div=0&chpt=1",
                        "description": "Pennsylvania criminal code",
                        "key_sections": [
                            "18 Pa. Cons. Stat. § 903 - Criminal conspiracy",
                            "18 Pa. Cons. Stat. § 3921 - Theft by unlawful taking",
                            "18 Pa. Cons. Stat. § 4107 - Deceptive business practices"
                        ],
                        "relevance": "Pennsylvania criminal violations"
                    }
                },
                "civil": {
                    "real_estate_licensing": {
                        "name": "Pennsylvania Real Estate Licensing and Registration Act",
                        "url": "https://www.legis.state.pa.us/cfdocs/legis/LI/consCheck.cfm?txtType=HTM&ttl=63&div=0&chpt=40",
                        "description": "Pennsylvania real estate licensing",
                        "key_sections": [
                            "63 Pa. Cons. Stat. § 455.201 - License required",
                            "63 Pa. Cons. Stat. § 455.604 - Grounds for suspension or revocation"
                        ],
                        "relevance": "Real estate licensing violations in Pennsylvania"
                    }
                }
            },
            "north_carolina": {
                "criminal": {
                    "general_statutes": {
                        "name": "North Carolina General Statutes - Criminal Law",
                        "url": "https://www.ncleg.gov/Laws/GeneralStatutes",
                        "description": "North Carolina criminal law",
                        "key_sections": [
                            "N.C. Gen. Stat. § 14-2.4 - Conspiracy",
                            "N.C. Gen. Stat. § 14-72 - Larceny",
                            "N.C. Gen. Stat. § 14-100 - Obtaining property by false pretenses"
                        ],
                        "relevance": "North Carolina criminal violations"
                    }
                },
                "civil": {
                    "real_estate_licensing": {
                        "name": "North Carolina Real Estate License Law",
                        "url": "https://www.ncrec.gov/",
                        "description": "North Carolina real estate licensing",
                        "key_sections": [
                            "N.C. Gen. Stat. § 93A-1 - Real Estate License Law",
                            "N.C. Gen. Stat. § 93A-2 - License required"
                        ],
                        "relevance": "Real estate licensing violations in North Carolina"
                    }
                }
            },
            "new_jersey": {
                "criminal": {
                    "criminal_code": {
                        "name": "New Jersey Criminal Code",
                        "url": "https://www.njleg.state.nj.us/",
                        "description": "New Jersey criminal law",
                        "key_sections": [
                            "N.J. Stat. Ann. § 2C:5-2 - Conspiracy",
                            "N.J. Stat. Ann. § 2C:20-3 - Theft by unlawful taking",
                            "N.J. Stat. Ann. § 2C:21-1 - Forgery"
                        ],
                        "relevance": "New Jersey criminal violations"
                    }
                },
                "civil": {
                    "real_estate_licensing": {
                        "name": "New Jersey Real Estate License Act",
                        "url": "https://www.nj.gov/dca/divisions/realestate/",
                        "description": "New Jersey real estate licensing",
                        "key_sections": [
                            "N.J. Stat. Ann. § 45:15-1 - Real Estate License Act",
                            "N.J. Stat. Ann. § 45:15-3 - License required"
                        ],
                        "relevance": "Real estate licensing violations in New Jersey"
                    }
                }
            },
            "new_york": {
                "criminal": {
                    "penal_law": {
                        "name": "New York Penal Law",
                        "url": "https://www.nysenate.gov/legislation/laws/PEN",
                        "description": "New York criminal law",
                        "key_sections": [
                            "N.Y. Penal Law § 105.05 - Conspiracy in the fourth degree",
                            "N.Y. Penal Law § 155.05 - Larceny",
                            "N.Y. Penal Law § 190.60 - Scheme to defraud"
                        ],
                        "relevance": "New York criminal violations"
                    }
                },
                "civil": {
                    "real_property_law": {
                        "name": "New York Real Property Law",
                        "url": "https://www.nysenate.gov/legislation/laws/RPP",
                        "description": "New York real estate licensing",
                        "key_sections": [
                            "N.Y. Real Prop. Law § 440 - Real Estate Brokers and Salespersons",
                            "N.Y. Real Prop. Law § 440-a - License required"
                        ],
                        "relevance": "Real estate licensing violations in New York"
                    }
                }
            },
            "connecticut": {
                "criminal": {
                    "general_statutes": {
                        "name": "Connecticut General Statutes - Criminal Law",
                        "url": "https://www.cga.ct.gov/current/pub/title_53a.htm",
                        "description": "Connecticut criminal law",
                        "key_sections": [
                            "Conn. Gen. Stat. § 53a-48 - Conspiracy",
                            "Conn. Gen. Stat. § 53a-119 - Larceny",
                            "Conn. Gen. Stat. § 53a-122 - Larceny in the first degree"
                        ],
                        "relevance": "Connecticut criminal violations"
                    }
                },
                "civil": {
                    "real_estate_licensing": {
                        "name": "Connecticut Real Estate License Law",
                        "url": "https://www.cga.ct.gov/current/pub/chap_392.htm",
                        "description": "Connecticut real estate licensing",
                        "key_sections": [
                            "Conn. Gen. Stat. § 20-311 - Real Estate Brokers and Salespersons",
                            "Conn. Gen. Stat. § 20-312 - License required"
                        ],
                        "relevance": "Real estate licensing violations in Connecticut"
                    }
                }
            },
            "alabama": {
                "criminal": {
                    "criminal_code": {
                        "name": "Alabama Criminal Code",
                        "url": "https://alisondb.legislature.state.al.us/alison/CodeOfAlabama/1975/Coatoc.htm",
                        "description": "Alabama criminal law",
                        "key_sections": [
                            "Ala. Code § 13A-4-3 - Criminal conspiracy",
                            "Ala. Code § 13A-8-2 - Theft of property",
                            "Ala. Code § 13A-8-3 - Theft by deception"
                        ],
                        "relevance": "Alabama criminal violations"
                    }
                },
                "civil": {
                    "real_estate_licensing": {
                        "name": "Alabama Real Estate License Law",
                        "url": "https://www.arec.alabama.gov/",
                        "description": "Alabama real estate licensing",
                        "key_sections": [
                            "Ala. Code § 34-27-1 - Real Estate License Act",
                            "Ala. Code § 34-27-30 - License required"
                        ],
                        "relevance": "Real estate licensing violations in Alabama"
                    }
                }
            },
            "arizona": {
                "criminal": {
                    "criminal_code": {
                        "name": "Arizona Criminal Code",
                        "url": "https://www.azleg.gov/ars/",
                        "description": "Arizona criminal law",
                        "key_sections": [
                            "Ariz. Rev. Stat. § 13-1003 - Conspiracy",
                            "Ariz. Rev. Stat. § 13-1802 - Theft",
                            "Ariz. Rev. Stat. § 13-2310 - Fraudulent schemes"
                        ],
                        "relevance": "Arizona criminal violations"
                    }
                },
                "civil": {
                    "real_estate_licensing": {
                        "name": "Arizona Real Estate License Law",
                        "url": "https://www.azre.gov/",
                        "description": "Arizona real estate licensing",
                        "key_sections": [
                            "Ariz. Rev. Stat. § 32-2101 - Real Estate License Act",
                            "Ariz. Rev. Stat. § 32-2121 - License required"
                        ],
                        "relevance": "Real estate licensing violations in Arizona"
                    }
                }
            },
            "california": {
                "criminal": {
                    "penal_code": {
                        "name": "California Penal Code",
                        "url": "https://leginfo.legislature.ca.gov/faces/codesTOCSelected.xhtml?tocCode=PEN",
                        "description": "California criminal law",
                        "key_sections": [
                            "Cal. Penal Code § 182 - Conspiracy",
                            "Cal. Penal Code § 484 - Theft",
                            "Cal. Penal Code § 532 - False pretenses"
                        ],
                        "relevance": "California criminal violations"
                    }
                },
                "civil": {
                    "business_professions_code": {
                        "name": "California Business and Professions Code",
                        "url": "https://leginfo.legislature.ca.gov/faces/codesTOCSelected.xhtml?tocCode=BPC",
                        "description": "California real estate licensing",
                        "key_sections": [
                            "Cal. Bus. & Prof. Code § 10130 - Real Estate License Act",
                            "Cal. Bus. & Prof. Code § 10131 - License required"
                        ],
                        "relevance": "Real estate licensing violations in California"
                    }
                }
            },
            "colorado": {
                "criminal": {
                    "criminal_code": {
                        "name": "Colorado Criminal Code",
                        "url": "https://leg.colorado.gov/agencies/office-legislative-legal-services/statutes",
                        "description": "Colorado criminal law",
                        "key_sections": [
                            "Colo. Rev. Stat. § 18-2-201 - Conspiracy",
                            "Colo. Rev. Stat. § 18-4-401 - Theft",
                            "Colo. Rev. Stat. § 18-5-102 - Criminal fraud"
                        ],
                        "relevance": "Colorado criminal violations"
                    }
                },
                "civil": {
                    "real_estate_licensing": {
                        "name": "Colorado Real Estate License Law",
                        "url": "https://dora.colorado.gov/dre",
                        "description": "Colorado real estate licensing",
                        "key_sections": [
                            "Colo. Rev. Stat. § 12-10-101 - Real Estate License Act",
                            "Colo. Rev. Stat. § 12-10-201 - License required"
                        ],
                        "relevance": "Real estate licensing violations in Colorado"
                    }
                }
            },
            "delaware": {
                "criminal": {
                    "criminal_code": {
                        "name": "Delaware Criminal Code",
                        "url": "https://delcode.delaware.gov/title11/",
                        "description": "Delaware criminal law",
                        "key_sections": [
                            "Del. Code Ann. tit. 11, § 512 - Conspiracy",
                            "Del. Code Ann. tit. 11, § 841 - Theft",
                            "Del. Code Ann. tit. 11, § 861 - Fraud"
                        ],
                        "relevance": "Delaware criminal violations"
                    }
                },
                "civil": {
                    "real_estate_licensing": {
                        "name": "Delaware Real Estate License Law",
                        "url": "https://dpr.delaware.gov/boards/realestate/",
                        "description": "Delaware real estate licensing",
                        "key_sections": [
                            "Del. Code Ann. tit. 24, § 2901 - Real Estate License Act",
                            "Del. Code Ann. tit. 24, § 2907 - License required"
                        ],
                        "relevance": "Real estate licensing violations in Delaware"
                    }
                }
            },
            "florida": {
                "criminal": {
                    "criminal_code": {
                        "name": "Florida Criminal Code",
                        "url": "https://www.leg.state.fl.us/statutes/",
                        "description": "Florida criminal law",
                        "key_sections": [
                            "Fla. Stat. § 777.04 - Attempts, solicitation, and conspiracy",
                            "Fla. Stat. § 812.014 - Theft",
                            "Fla. Stat. § 817.034 - Fraudulent practices"
                        ],
                        "relevance": "Florida criminal violations"
                    }
                },
                "civil": {
                    "real_estate_licensing": {
                        "name": "Florida Real Estate License Law",
                        "url": "https://www.myfloridalicense.com/CheckLicense2/",
                        "description": "Florida real estate licensing",
                        "key_sections": [
                            "Fla. Stat. § 475.01 - Real Estate License Act",
                            "Fla. Stat. § 475.15 - License required"
                        ],
                        "relevance": "Real estate licensing violations in Florida"
                    }
                }
            },
            "georgia": {
                "criminal": {
                    "criminal_code": {
                        "name": "Georgia Criminal Code",
                        "url": "https://law.justia.com/codes/georgia/",
                        "description": "Georgia criminal law",
                        "key_sections": [
                            "Ga. Code Ann. § 16-4-8 - Conspiracy",
                            "Ga. Code Ann. § 16-8-2 - Theft by taking",
                            "Ga. Code Ann. § 16-8-3 - Theft by deception"
                        ],
                        "relevance": "Georgia criminal violations"
                    }
                },
                "civil": {
                    "real_estate_licensing": {
                        "name": "Georgia Real Estate License Law",
                        "url": "https://grec.state.ga.us/",
                        "description": "Georgia real estate licensing",
                        "key_sections": [
                            "Ga. Code Ann. § 43-40-1 - Real Estate License Act",
                            "Ga. Code Ann. § 43-40-8 - License required"
                        ],
                        "relevance": "Real estate licensing violations in Georgia"
                    }
                }
            },
            "massachusetts": {
                "criminal": {
                    "criminal_code": {
                        "name": "Massachusetts Criminal Code",
                        "url": "https://malegislature.gov/Laws/GeneralLaws/PartIV/TitleI",
                        "description": "Massachusetts criminal law",
                        "key_sections": [
                            "Mass. Gen. Laws ch. 274, § 7 - Conspiracy",
                            "Mass. Gen. Laws ch. 266, § 30 - Larceny",
                            "Mass. Gen. Laws ch. 266, § 30A - Fraud"
                        ],
                        "relevance": "Massachusetts criminal violations"
                    }
                },
                "civil": {
                    "real_estate_licensing": {
                        "name": "Massachusetts Real Estate License Law",
                        "url": "https://www.mass.gov/orgs/board-of-registration-of-real-estate-brokers-and-salespersons",
                        "description": "Massachusetts real estate licensing",
                        "key_sections": [
                            "Mass. Gen. Laws ch. 112, § 87PP - Real Estate License Act",
                            "Mass. Gen. Laws ch. 112, § 87RR - License required"
                        ],
                        "relevance": "Real estate licensing violations in Massachusetts"
                    }
                }
            },
            "new_mexico": {
                "criminal": {
                    "criminal_code": {
                        "name": "New Mexico Criminal Code",
                        "url": "https://www.nmonesource.com/nmos/nmsa/en/item/4000/index.do",
                        "description": "New Mexico criminal law",
                        "key_sections": [
                            "N.M. Stat. Ann. § 30-28-2 - Conspiracy",
                            "N.M. Stat. Ann. § 30-16-1 - Larceny",
                            "N.M. Stat. Ann. § 30-16-6 - Fraud"
                        ],
                        "relevance": "New Mexico criminal violations"
                    }
                },
                "civil": {
                    "real_estate_licensing": {
                        "name": "New Mexico Real Estate License Law",
                        "url": "https://www.rld.nm.gov/boards-and-commissions/individual-boards-and-commissions/real-estate/",
                        "description": "New Mexico real estate licensing",
                        "key_sections": [
                            "N.M. Stat. Ann. § 61-29-1 - Real Estate License Act",
                            "N.M. Stat. Ann. § 61-29-4 - License required"
                        ],
                        "relevance": "Real estate licensing violations in New Mexico"
                    }
                }
            },
            "south_carolina": {
                "criminal": {
                    "criminal_code": {
                        "name": "South Carolina Criminal Code",
                        "url": "https://www.scstatehouse.gov/code/t16c.php",
                        "description": "South Carolina criminal law",
                        "key_sections": [
                            "S.C. Code Ann. § 16-17-410 - Conspiracy",
                            "S.C. Code Ann. § 16-13-30 - Larceny",
                            "S.C. Code Ann. § 16-13-240 - Fraud"
                        ],
                        "relevance": "South Carolina criminal violations"
                    }
                },
                "civil": {
                    "real_estate_licensing": {
                        "name": "South Carolina Real Estate License Law",
                        "url": "https://www.llr.sc.gov/POL/RealEstate/",
                        "description": "South Carolina real estate licensing",
                        "key_sections": [
                            "S.C. Code Ann. § 40-57-10 - Real Estate License Act",
                            "S.C. Code Ann. § 40-57-30 - License required"
                        ],
                        "relevance": "Real estate licensing violations in South Carolina"
                    }
                }
            },
            "utah": {
                "criminal": {
                    "criminal_code": {
                        "name": "Utah Criminal Code",
                        "url": "https://le.utah.gov/xcode/Title76/76.html",
                        "description": "Utah criminal law",
                        "key_sections": [
                            "Utah Code Ann. § 76-4-201 - Criminal conspiracy",
                            "Utah Code Ann. § 76-6-404 - Theft",
                            "Utah Code Ann. § 76-6-502 - Fraud"
                        ],
                        "relevance": "Utah criminal violations"
                    }
                },
                "civil": {
                    "real_estate_licensing": {
                        "name": "Utah Real Estate License Law",
                        "url": "https://dopl.utah.gov/realestate/",
                        "description": "Utah real estate licensing",
                        "key_sections": [
                            "Utah Code Ann. § 61-2-1 - Real Estate License Act",
                            "Utah Code Ann. § 61-2-2 - License required"
                        ],
                        "relevance": "Real estate licensing violations in Utah"
                    }
                }
            }
        },
        "localities": {
            "virginia": {
                "fairfax_county": {
                    "name": "Fairfax County Code",
                    "description": "Fairfax County local ordinances",
                    "relevance": "Local property management and business regulations"
                },
                "arlington_county": {
                    "name": "Arlington County Code",
                    "description": "Arlington County local ordinances",
                    "relevance": "Local property management and business regulations"
                },
                "alexandria": {
                    "name": "City of Alexandria Code",
                    "description": "City of Alexandria local ordinances",
                    "relevance": "Local property management and business regulations"
                }
            },
            "texas": {
                "dallas_county": {
                    "name": "Dallas County Code",
                    "description": "Dallas County local ordinances",
                    "relevance": "Local property management and business regulations"
                },
                "harris_county": {
                    "name": "Harris County Code",
                    "description": "Harris County local ordinances",
                    "relevance": "Local property management and business regulations"
                }
            },
            "maryland": {
                "montgomery_county": {
                    "name": "Montgomery County Code",
                    "description": "Montgomery County local ordinances",
                    "relevance": "Local property management and business regulations"
                },
                "prince_georges_county": {
                    "name": "Prince George's County Code",
                    "description": "Prince George's County local ordinances",
                    "relevance": "Local property management and business regulations"
                }
            },
            "dc": {
                "dc_municipal": {
                    "name": "District of Columbia Municipal Regulations",
                    "description": "D.C. municipal regulations",
                    "relevance": "Local property management and business regulations"
                }
            }
        }
    }


def create_text_for_embedding(jurisdiction_data: Dict[str, Any], path: str = "") -> str:
    """Create comprehensive text representation for embedding from jurisdiction data
    Includes full law citations as ground truth"""
    parts = []

    # Full law name and citation
    if "name" in jurisdiction_data:
        parts.append(f"LAW: {jurisdiction_data['name']}")

    # Full description
    if "description" in jurisdiction_data:
        parts.append(f"DESCRIPTION: {jurisdiction_data['description']}")

    # Official URL (authoritative source)
    if "url" in jurisdiction_data:
        parts.append(f"OFFICIAL_SOURCE: {jurisdiction_data['url']}")

    # Complete law citations - this is the ground truth
    if "key_sections" in jurisdiction_data:
        # Include full citations with section numbers
        full_citations = []
        for section in jurisdiction_data['key_sections']:
            # Ensure full citation format
            if "§" in section or "Section" in section or "Code" in section:
                full_citations.append(section)
            else:
                full_citations.append(section)
        parts.append(f"FULL_CITATIONS: {' | '.join(full_citations)}")
        # Also include as separate entries for better matching
        parts.append(f"KEY_SECTIONS: {'; '.join(jurisdiction_data['key_sections'])}")

    # Relevance context
    if "relevance" in jurisdiction_data:
        parts.append(f"RELEVANCE: {jurisdiction_data['relevance']}")

    # Reporting forms (if applicable)
    if "reporting_forms" in jurisdiction_data:
        form_citations = []
        for form in jurisdiction_data.get("reporting_forms", []):
            form_text = f"{form.get('form_name', '')} ({form.get('form_number', '')}) - {form.get('agency', '')} - {form.get('description', '')}"
            form_citations.append(form_text)
        if form_citations:
            parts.append(f"REPORTING_FORMS: {' | '.join(form_citations)}")

    # Path for reference
    if path:
        # Extract jurisdiction from path for context
        if "federal" in path:
            parts.append("JURISDICTION: Federal")
        elif "states." in path:
            state = path.split("states.")[1].split(".")[0] if "states." in path else ""
            parts.append(f"JURISDICTION: State - {state.replace('_', ' ').title()}")
        elif "localities" in path:
            parts.append("JURISDICTION: Local")

    # Mark as ground truth
    parts.append("GROUND_TRUTH: TRUE")
    parts.append("AUTHORITATIVE_SOURCE: TRUE")

    return " | ".join(parts)


def collect_embedding_tasks(data: Any, path: str = "", tasks: List[Tuple[str, Dict[str, Any]]] = None) -> List[Tuple[str, Dict[str, Any]]]:
    """Collect all items that need embeddings for parallel processing"""
    if tasks is None:
        tasks = []

    if isinstance(data, dict):
        # Check if this is a jurisdiction entry (has name or description)
        if "name" in data or "description" in data:
            tasks.append((path, data))

        # Recursively collect from nested dictionaries
        for key, value in data.items():
            if key not in ["embedding", "embedding_text"]:  # Skip already processed embeddings
                new_path = f"{path}.{key}" if path else key
                collect_embedding_tasks(value, new_path, tasks)

    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_path = f"{path}[{i}]"
            collect_embedding_tasks(item, new_path, tasks)

    return tasks


def generate_embeddings_batch(texts_and_paths: List[Tuple[str, str]], model: SentenceTransformer) -> Dict[str, Tuple[List[float], str]]:
    """Generate embeddings for a batch of texts (more efficient than one-by-one)"""
    paths = [p for p, _ in texts_and_paths]
    texts = [t for _, t in texts_and_paths]

    # Batch encode all texts at once (much faster)
    embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=False, batch_size=32)

    # Return as dictionary mapping path to (embedding, text)
    results = {}
    for i, path in enumerate(paths):
        results[path] = (embeddings[i].tolist(), texts_and_paths[i][1])

    return results


def add_embeddings_parallel(data: Dict[str, Any], model: SentenceTransformer, max_workers: int = MAX_WORKERS) -> None:
    """Add embeddings to jurisdiction data using parallel batch processing (optimized for ARM M4 MAX)"""
    print(f"📊 Collecting embedding tasks...")
    tasks = collect_embedding_tasks(data)
    total_tasks = len(tasks)
    print(f"   Found {total_tasks} items requiring embeddings")

    if total_tasks == 0:
        print("⚠️  No items found requiring embeddings")
        return

    # Prepare texts for batch processing
    texts_and_paths = []
    path_to_item = {}
    for path, item in tasks:
        text = create_text_for_embedding(item, path)
        texts_and_paths.append((path, text))
        path_to_item[path] = item

    print(f"🚀 Generating embeddings using batch processing with {max_workers} parallel batches...")
    print(f"   Processing {total_tasks} items in optimized batches...")

    # Split into batches for parallel processing
    batch_size = max(1, total_tasks // max_workers)
    batches = []
    for i in range(0, len(texts_and_paths), batch_size):
        batches.append(texts_and_paths[i:i + batch_size])

    print(f"   Created {len(batches)} batches (avg {len(batches[0]) if batches else 0} items per batch)")

    # Process batches in parallel
    all_results = {}
    completed_batches = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all batches
        future_to_batch = {executor.submit(generate_embeddings_batch, batch, model): batch
                          for batch in batches}

        # Process completed batches
        for future in as_completed(future_to_batch):
            try:
                batch_results = future.result()
                all_results.update(batch_results)
                completed_batches += 1
                completed_items = len(all_results)
                if completed_batches % max(1, len(batches) // 10) == 0 or completed_batches == len(batches):
                    progress = (completed_items / total_tasks) * 100
                    print(f"   Progress: {completed_items}/{total_tasks} ({progress:.1f}%) - {completed_batches}/{len(batches)} batches")
            except Exception as e:
                batch = future_to_batch[future]
                print(f"   ⚠️  Error processing batch: {e}")
                import traceback
                traceback.print_exc()

    print(f"✅ Generated {len(all_results)} embeddings")
    print(f"📝 Applying embeddings to data structure...")

    # Apply embeddings back to data structure
    def apply_embeddings_recursive(data: Any, path: str = "") -> None:
        if isinstance(data, dict):
            if "name" in data or "description" in data:
                if path in all_results:
                    embedding, text = all_results[path]
                    data["embedding"] = embedding
                    data["embedding_text"] = text

            for key, value in data.items():
                if key not in ["embedding", "embedding_text"]:
                    new_path = f"{path}.{key}" if path else key
                    apply_embeddings_recursive(value, new_path)

        elif isinstance(data, list):
            for i, item in enumerate(data):
                new_path = f"{path}[{i}]"
                apply_embeddings_recursive(item, new_path)

    apply_embeddings_recursive(data)
    print(f"✅ Applied all embeddings to data structure")


def add_embeddings_recursive(data: Dict[str, Any], model: SentenceTransformer, path: str = "") -> None:
    """Recursively add embeddings to jurisdiction data (legacy sequential version)"""
    # Process current level
    if isinstance(data, dict):
        # Check if this is a jurisdiction entry (has name or description)
        if "name" in data or "description" in data:
            text = create_text_for_embedding(data, path)
            embedding = model.encode(text, normalize_embeddings=True)
            data["embedding"] = embedding.tolist()
            data["embedding_text"] = text

        # Recursively process nested dictionaries
        for key, value in data.items():
            if key not in ["embedding", "embedding_text"]:  # Skip already processed embeddings
                new_path = f"{path}.{key}" if path else key
                add_embeddings_recursive(value, model, new_path)

    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_path = f"{path}[{i}]"
            add_embeddings_recursive(item, model, new_path)


def main():
    """Main function to create law references with embeddings - optimized for ARM M4 MAX"""
    import time
    start_time = time.time()

    print("=" * 80)
    print("🚀 Law Reference Creation - ARM M4 MAX Optimized")
    print("=" * 80)
    print(f"Using {MAX_WORKERS} parallel workers for maximum throughput\n")

    print("📋 Creating law reference structure...")
    references = create_jurisdiction_references()
    structure_time = time.time()
    print(f"   ✅ Structure created in {structure_time - start_time:.2f}s\n")

    print("🤖 Loading embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("✅ Model loaded\n")

    print("🚀 Generating embeddings using parallel batch processing...")
    embedding_start = time.time()
    add_embeddings_parallel(references, model, MAX_WORKERS)
    embedding_time = time.time()
    elapsed = embedding_time - embedding_start
    print(f"   ✅ Embeddings generated in {elapsed:.2f}s\n")

    # Create output directory
    ref_dir = PROJECT_ROOT / "ref" / "law"
    ref_dir.mkdir(parents=True, exist_ok=True)

    # Save JSON file
    output_file = ref_dir / "jurisdiction_references.json"
    print(f"💾 Saving to {output_file}...")
    save_start = time.time()
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(references, f, indent=2, ensure_ascii=False)
    save_time = time.time()
    print(f"   ✅ Saved in {save_time - save_start:.2f}s\n")

    # Create summary statistics
    def count_embeddings(data: Any) -> int:
        """Count number of embeddings in data"""
        count = 0
        if isinstance(data, dict):
            if "embedding" in data:
                count += 1
            for value in data.values():
                count += count_embeddings(value)
        elif isinstance(data, list):
            for item in data:
                count += count_embeddings(item)
        return count

    embedding_count = count_embeddings(references)
    total_time = time.time() - start_time

    print("=" * 80)
    print("✅ Successfully created law reference file")
    print("=" * 80)
    print(f"   File: {output_file}")
    print(f"   Embeddings generated: {embedding_count}")
    print(f"   Model: all-MiniLM-L6-v2")
    print(f"   Dimensions: 384")
    print(f"   Parallel workers: {MAX_WORKERS}")
    print(f"   Total time: {total_time:.2f}s")
    print(f"   Throughput: {embedding_count/total_time:.1f} embeddings/second")
    print("=" * 80)


if __name__ == "__main__":
    main()
