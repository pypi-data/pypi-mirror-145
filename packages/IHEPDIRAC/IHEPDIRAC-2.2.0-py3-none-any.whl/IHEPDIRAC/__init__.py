""""

"""

def extension_metadata():
  return {
      "primary_extension": True,
      "priority": 100,
      "setups": {
          "CAS_Production": "dips://dirac.ihep.ac.cn:9135/Configuration/Server",
          "CAS_Production-cert": "dips://dirac.ihep.ac.cn:9135/Configuration/Server",
      },
      "default_setup": "CAS_Production",
  }

