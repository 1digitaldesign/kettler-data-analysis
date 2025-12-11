#!/usr/bin/env python3
"""
Create law reference JSON with embedded vectors for jurisdictions
Focuses on criminal law first, then civil law
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

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
                    "relevance": "Federal criminal violations related to fraud, conspiracy, money laundering, and organized crime"
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
                    "relevance": "Criminal tax violations including evasion, fraud, and false filings"
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
                    "relevance": "Securities fraud and deceptive trade practices"
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
                    "relevance": "Consumer protection, antitrust, and fair trade practices"
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
                    "relevance": "Civil rights, fair housing, and discrimination claims"
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
                        "relevance": "Real estate licensing violations and professional misconduct"
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
                        "relevance": "Property management and landlord-tenant violations"
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
                        "relevance": "Real estate licensing violations in Texas"
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
                        "relevance": "Business entity violations and corporate compliance"
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
            "district_of_columbia": {
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
            "district_of_columbia": {
                "dc_municipal": {
                    "name": "District of Columbia Municipal Regulations",
                    "description": "D.C. municipal regulations",
                    "relevance": "Local property management and business regulations"
                }
            }
        }
    }


def create_text_for_embedding(jurisdiction_data: Dict[str, Any], path: str = "") -> str:
    """Create text representation for embedding from jurisdiction data"""
    parts = []

    if "name" in jurisdiction_data:
        parts.append(f"Name: {jurisdiction_data['name']}")

    if "description" in jurisdiction_data:
        parts.append(f"Description: {jurisdiction_data['description']}")

    if "url" in jurisdiction_data:
        parts.append(f"URL: {jurisdiction_data['url']}")

    if "key_sections" in jurisdiction_data:
        parts.append(f"Key Sections: {'; '.join(jurisdiction_data['key_sections'])}")

    if "relevance" in jurisdiction_data:
        parts.append(f"Relevance: {jurisdiction_data['relevance']}")

    if path:
        parts.append(f"Path: {path}")

    return " | ".join(parts)


def add_embeddings_recursive(data: Dict[str, Any], model: SentenceTransformer, path: str = "") -> None:
    """Recursively add embeddings to jurisdiction data"""

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
    """Main function to create law references with embeddings"""
    print("Creating law reference structure...")
    references = create_jurisdiction_references()

    print("Loading embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    print("Generating embeddings for all jurisdictions...")
    add_embeddings_recursive(references, model)

    # Create output directory
    ref_dir = PROJECT_ROOT / "ref" / "law"
    ref_dir.mkdir(parents=True, exist_ok=True)

    # Save JSON file
    output_file = ref_dir / "jurisdiction_references.json"
    print(f"Saving to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(references, f, indent=2, ensure_ascii=False)

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

    print(f"\n✅ Successfully created law reference file")
    print(f"   File: {output_file}")
    print(f"   Embeddings generated: {embedding_count}")
    print(f"   Model: all-MiniLM-L6-v2")
    print(f"   Dimensions: 384")


if __name__ == "__main__":
    main()
