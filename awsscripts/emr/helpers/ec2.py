from typing import Dict

# https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-supported-instance-types.html
# TODO: include supported emr versions for each

ec2_instances: Dict[str, Dict[str, float]] = {
    "t1.micro": {"cpu": 1, "memory": 0.612, "ghz": 0, "storage": 0},
    "t2.nano": {"cpu": 1, "memory": 0.5, "ghz": 2.4, "storage": 0},
    "t2.micro": {"cpu": 1, "memory": 1, "ghz": 2.5, "storage": 0},
    "t2.small": {"cpu": 1, "memory": 2, "ghz": 2.5, "storage": 0},
    "t2.medium": {"cpu": 2, "memory": 4, "ghz": 2.3, "storage": 0},
    "t2.large": {"cpu": 2, "memory": 8, "ghz": 2.3, "storage": 0},
    "t2.xlarge": {"cpu": 4, "memory": 16, "ghz": 2.3, "storage": 0},
    "t2.2xlarge": {"cpu": 8, "memory": 32, "ghz": 2.3, "storage": 0},
    "t3.nano": {"cpu": 2, "memory": 0.5, "ghz": 2.5, "storage": 0},
    "t3.micro": {"cpu": 2, "memory": 1, "ghz": 2.5, "storage": 0},
    "t3.small": {"cpu": 2, "memory": 2, "ghz": 2.5, "storage": 0},
    "t3.medium": {"cpu": 2, "memory": 4, "ghz": 2.5, "storage": 0},
    "t3.large": {"cpu": 2, "memory": 8, "ghz": 2.5, "storage": 0},
    "t3.xlarge": {"cpu": 4, "memory": 16, "ghz": 2.5, "storage": 0},
    "t3.2xlarge": {"cpu": 8, "memory": 32, "ghz": 2.5, "storage": 0},
    "a1.medium": {"cpu": 1, "memory": 2, "ghz": 2.3, "storage": 0},
    "a1.large": {"cpu": 2, "memory": 4, "ghz": 2.3, "storage": 0},
    "a1.xlarge": {"cpu": 4, "memory": 8, "ghz": 2.3, "storage": 0},
    "a1.2xlarge": {"cpu": 8, "memory": 16, "ghz": 2.3, "storage": 0},
    "a1.4xlarge": {"cpu": 16, "memory": 32, "ghz": 2.3, "storage": 0},
    "a1.metal": {"cpu": 16, "memory": 32, "ghz": 2.3, "storage": 0},
    "c1.medium": {"cpu": 2, "memory": 1.7, "ghz": 0, "storage": 350},
    "c1.xlarge": {"cpu": 8, "memory": 7, "ghz": 0, "storage": 1680},
    "c3.large": {"cpu": 2, "memory": 3.75, "ghz": 2.8, "storage": 32},
    "c3.xlarge": {"cpu": 4, "memory": 7.5, "ghz": 2.8, "storage": 80},
    "c3.2xlarge": {"cpu": 8, "memory": 15, "ghz": 2.8, "storage": 160},
    "c3.4xlarge": {"cpu": 16, "memory": 30, "ghz": 2.8, "storage": 320},
    "c3.8xlarge": {"cpu": 32, "memory": 60, "ghz": 2.8, "storage": 640},
    "c4.large": {"cpu": 2, "memory": 3.75, "ghz": 2.9, "storage": 0},
    "c4.xlarge": {"cpu": 4, "memory": 7.5, "ghz": 2.9, "storage": 0},
    "c4.2xlarge": {"cpu": 8, "memory": 15, "ghz": 2.9, "storage": 0},
    "c4.4xlarge": {"cpu": 16, "memory": 30, "ghz": 2.9, "storage": 0},
    "c4.8xlarge": {"cpu": 36, "memory": 60, "ghz": 2.9, "storage": 0},
    "c5.large": {"cpu": 2, "memory": 4, "ghz": 3.4, "storage": 0},
    "c5.xlarge": {"cpu": 4, "memory": 8, "ghz": 3.4, "storage": 0},
    "c5.2xlarge": {"cpu": 8, "memory": 16, "ghz": 3.4, "storage": 0},
    "c5.4xlarge": {"cpu": 16, "memory": 32, "ghz": 3.4, "storage": 0},
    "c5.9xlarge": {"cpu": 36, "memory": 72, "ghz": 3.4, "storage": 0},
    "c5.12xlarge": {"cpu": 48, "memory": 96, "ghz": 3.6, "storage": 0},
    "c5.18xlarge": {"cpu": 72, "memory": 144, "ghz": 3.4, "storage": 0},
    "c5.24xlarge": {"cpu": 96, "memory": 192, "ghz": 3.6, "storage": 0},
    "c5.metal": {"cpu": 96, "memory": 192, "ghz": 3.6, "storage": 0},
    "c5a.large": {"cpu": 2, "memory": 4, "ghz": 3.3, "storage": 0},
    "c5a.xlarge": {"cpu": 4, "memory": 8, "ghz": 3.3, "storage": 0},
    "c5a.2xlarge": {"cpu": 8, "memory": 16, "ghz": 3.3, "storage": 0},
    "c5a.4xlarge": {"cpu": 16, "memory": 32, "ghz": 3.3, "storage": 0},
    "c5a.8xlarge": {"cpu": 32, "memory": 64, "ghz": 3.3, "storage": 0},
    "c5a.12xlarge": {"cpu": 48, "memory": 96, "ghz": 3.3, "storage": 0},
    "c5a.16xlarge": {"cpu": 64, "memory": 128, "ghz": 3.3, "storage": 0},
    "c5a.24xlarge": {"cpu": 96, "memory": 192, "ghz": 3.3, "storage": 0},
    "c5ad.large": {"cpu": 2, "memory": 4, "ghz": 3.3, "storage": 75},
    "c5ad.xlarge": {"cpu": 4, "memory": 8, "ghz": 3.3, "storage": 150},
    "c5ad.2xlarge": {"cpu": 8, "memory": 16, "ghz": 3.3, "storage": 300},
    "c5ad.4xlarge": {"cpu": 16, "memory": 32, "ghz": 3.3, "storage": 600},
    "c5ad.8xlarge": {"cpu": 32, "memory": 64, "ghz": 3.3, "storage": 1200},
    "c5ad.12xlarge": {"cpu": 48, "memory": 96, "ghz": 3.3, "storage": 1800},
    "c5ad.16xlarge": {"cpu": 64, "memory": 128, "ghz": 3.3, "storage": 2400},
    "c5ad.24xlarge": {"cpu": 96, "memory": 192, "ghz": 3.3, "storage": 3800},
    "c5d.large": {"cpu": 2, "memory": 4, "ghz": 3.4, "storage": 50},
    "c5d.xlarge": {"cpu": 4, "memory": 8, "ghz": 3.4, "storage": 100},
    "c5d.2xlarge": {"cpu": 8, "memory": 16, "ghz": 3.4, "storage": 200},
    "c5d.4xlarge": {"cpu": 16, "memory": 32, "ghz": 3.4, "storage": 400},
    "c5d.9xlarge": {"cpu": 36, "memory": 72, "ghz": 3.4, "storage": 900},
    "c5d.12xlarge": {"cpu": 48, "memory": 96, "ghz": 3.6, "storage": 1800},
    "c5d.18xlarge": {"cpu": 72, "memory": 144, "ghz": 3.4, "storage": 1800},
    "c5d.24xlarge": {"cpu": 96, "memory": 192, "ghz": 3.6, "storage": 3600},
    "c5d.metal": {"cpu": 96, "memory": 192, "ghz": 3.6, "storage": 3600},
    "c5n.large": {"cpu": 2, "memory": 5.3, "ghz": 3.4, "storage": 0},
    "c5n.xlarge": {"cpu": 4, "memory": 10.5, "ghz": 3.4, "storage": 0},
    "c5n.2xlarge": {"cpu": 8, "memory": 21, "ghz": 3.4, "storage": 0},
    "c5n.4xlarge": {"cpu": 16, "memory": 42, "ghz": 3.4, "storage": 0},
    "c5n.9xlarge": {"cpu": 36, "memory": 96, "ghz": 3.4, "storage": 0},
    "c5n.18xlarge": {"cpu": 72, "memory": 192, "ghz": 3.4, "storage": 0},
    "c5n.metal": {"cpu": 72, "memory": 192, "ghz": 3.4, "storage": 0},
    "c6g.medium": {"cpu": 1, "memory": 2, "ghz": 2.5, "storage": 0},
    "c6g.large": {"cpu": 2, "memory": 4, "ghz": 2.5, "storage": 0},
    "c6g.xlarge": {"cpu": 4, "memory": 8, "ghz": 2.5, "storage": 0},
    "c6g.2xlarge": {"cpu": 8, "memory": 16, "ghz": 2.5, "storage": 0},
    "c6g.4xlarge": {"cpu": 16, "memory": 32, "ghz": 2.5, "storage": 0},
    "c6g.8xlarge": {"cpu": 32, "memory": 64, "ghz": 2.5, "storage": 0},
    "c6g.12xlarge": {"cpu": 48, "memory": 96, "ghz": 2.5, "storage": 0},
    "c6g.16xlarge": {"cpu": 64, "memory": 128, "ghz": 2.5, "storage": 0},
    "c6g.metal": {"cpu": 64, "memory": 128, "ghz": 2.5, "storage": 0},
    "c6gd.medium": {"cpu": 1, "memory": 2, "ghz": 2.5, "storage": 59},
    "c6gd.large": {"cpu": 2, "memory": 4, "ghz": 2.5, "storage": 118},
    "c6gd.xlarge": {"cpu": 4, "memory": 8, "ghz": 2.5, "storage": 237},
    "c6gd.2xlarge": {"cpu": 8, "memory": 16, "ghz": 2.5, "storage": 474},
    "c6gd.4xlarge": {"cpu": 16, "memory": 32, "ghz": 2.5, "storage": 950},
    "c6gd.8xlarge": {"cpu": 32, "memory": 64, "ghz": 2.5, "storage": 1900},
    "c6gd.12xlarge": {"cpu": 48, "memory": 96, "ghz": 2.5, "storage": 2850},
    "c6gd.16xlarge": {"cpu": 64, "memory": 128, "ghz": 2.5, "storage": 3800},
    "c6gd.metal": {"cpu": 64, "memory": 128, "ghz": 2.5, "storage": 3800},
    "c6gn.medium": {"cpu": 1, "memory": 2, "ghz": 2.5, "storage": 0},
    "c6gn.large": {"cpu": 2, "memory": 4, "ghz": 2.5, "storage": 0},
    "c6gn.xlarge": {"cpu": 4, "memory": 8, "ghz": 2.5, "storage": 0},
    "c6gn.2xlarge": {"cpu": 8, "memory": 16, "ghz": 2.5, "storage": 0},
    "c6gn.4xlarge": {"cpu": 16, "memory": 32, "ghz": 2.5, "storage": 0},
    "c6gn.8xlarge": {"cpu": 32, "memory": 64, "ghz": 2.5, "storage": 0},
    "c6gn.12xlarge": {"cpu": 48, "memory": 96, "ghz": 2.5, "storage": 0},
    "c6gn.16xlarge": {"cpu": 64, "memory": 128, "ghz": 2.5, "storage": 0},
    "cc2.8xlarge": {"cpu": 32, "memory": 60.5, "ghz": 2.6, "storage": 3360},
    "d2.xlarge": {"cpu": 4, "memory": 30.5, "ghz": 2.4, "storage": 6144},
    "d2.2xlarge": {"cpu": 8, "memory": 61, "ghz": 2.4, "storage": 12288},
    "d2.4xlarge": {"cpu": 16, "memory": 122, "ghz": 2.4, "storage": 24576},
    "d2.8xlarge": {"cpu": 36, "memory": 244, "ghz": 2.4, "storage": 49152},
    "d3.xlarge": {"cpu": 4, "memory": 32, "ghz": 3.1, "storage": 5940},
    "d3.2xlarge": {"cpu": 8, "memory": 64, "ghz": 3.1, "storage": 11880},
    "d3.4xlarge": {"cpu": 16, "memory": 128, "ghz": 3.1, "storage": 23760},
    "d3.8xlarge": {"cpu": 32, "memory": 256, "ghz": 3.1, "storage": 47520},
    "d3en.xlarge": {"cpu": 4, "memory": 16, "ghz": 3.1, "storage": 27960},
    "d3en.2xlarge": {"cpu": 8, "memory": 32, "ghz": 3.1, "storage": 55920},
    "d3en.4xlarge": {"cpu": 16, "memory": 64, "ghz": 3.1, "storage": 111840},
    "d3en.6xlarge": {"cpu": 24, "memory": 96, "ghz": 3.1, "storage": 167760},
    "d3en.8xlarge": {"cpu": 32, "memory": 128, "ghz": 3.1, "storage": 223680},
    "d3en.12xlarge": {"cpu": 48, "memory": 192, "ghz": 3.1, "storage": 335520},
    "f1.2xlarge": {"cpu": 8, "memory": 122, "ghz": 2.3, "storage": 470},
    "f1.4xlarge": {"cpu": 16, "memory": 244, "ghz": 2.3, "storage": 940},
    "f1.16xlarge": {"cpu": 64, "memory": 976, "ghz": 2.3, "storage": 3760},
    "g2.2xlarge": {"cpu": 8, "memory": 15, "ghz": 2.6, "storage": 60},
    "g2.8xlarge": {"cpu": 32, "memory": 60, "ghz": 2.6, "storage": 240},
    "g3.4xlarge": {"cpu": 16, "memory": 122, "ghz": 2.7, "storage": 0},
    "g3.8xlarge": {"cpu": 32, "memory": 244, "ghz": 2.7, "storage": 0},
    "g3.16xlarge": {"cpu": 64, "memory": 488, "ghz": 2.3, "storage": 0},
    "g3s.xlarge": {"cpu": 4, "memory": 30.5, "ghz": 2.7, "storage": 0},
    "g4ad.4xlarge": {"cpu": 16, "memory": 64, "ghz": 3, "storage": 600},
    "g4ad.8xlarge": {"cpu": 32, "memory": 128, "ghz": 3, "storage": 1200},
    "g4ad.16xlarge": {"cpu": 64, "memory": 256, "ghz": 3, "storage": 2400},
    "g4dn.xlarge": {"cpu": 4, "memory": 16, "ghz": 2.5, "storage": 125},
    "g4dn.2xlarge": {"cpu": 8, "memory": 32, "ghz": 2.5, "storage": 225},
    "g4dn.4xlarge": {"cpu": 16, "memory": 64, "ghz": 2.5, "storage": 225},
    "g4dn.8xlarge": {"cpu": 32, "memory": 128, "ghz": 2.5, "storage": 900},
    "g4dn.12xlarge": {"cpu": 48, "memory": 192, "ghz": 2.5, "storage": 900},
    "g4dn.16xlarge": {"cpu": 64, "memory": 256, "ghz": 2.5, "storage": 900},
    "g4dn.metal": {"cpu": 96, "memory": 384, "ghz": 2.5, "storage": 1800},
    "h1.2xlarge": {"cpu": 8, "memory": 32, "ghz": 2.3, "storage": 2000},
    "h1.4xlarge": {"cpu": 16, "memory": 64, "ghz": 2.3, "storage": 4000},
    "h1.8xlarge": {"cpu": 32, "memory": 128, "ghz": 2.3, "storage": 8000},
    "h1.16xlarge": {"cpu": 64, "memory": 256, "ghz": 2.3, "storage": 16000},
    "i2.xlarge": {"cpu": 4, "memory": 30.5, "ghz": 2.5, "storage": 800},
    "i2.2xlarge": {"cpu": 8, "memory": 61, "ghz": 2.5, "storage": 1600},
    "i2.4xlarge": {"cpu": 16, "memory": 122, "ghz": 2.5, "storage": 3200},
    "i2.8xlarge": {"cpu": 32, "memory": 244, "ghz": 2.5, "storage": 6400},
    "i3.large": {"cpu": 2, "memory": 15.3, "ghz": 2.3, "storage": 475},
    "i3.xlarge": {"cpu": 4, "memory": 30.5, "ghz": 2.3, "storage": 950},
    "i3.2xlarge": {"cpu": 8, "memory": 61, "ghz": 2.3, "storage": 1900},
    "i3.4xlarge": {"cpu": 16, "memory": 122, "ghz": 2.3, "storage": 3800},
    "i3.8xlarge": {"cpu": 32, "memory": 244, "ghz": 2.3, "storage": 7600},
    "i3.16xlarge": {"cpu": 64, "memory": 488, "ghz": 2.3, "storage": 15200},
    "i3.metal": {"cpu": 72, "memory": 512, "ghz": 2.3, "storage": 15200},
    "i3en.large": {"cpu": 2, "memory": 16, "ghz": 3.1, "storage": 1250},
    "i3en.xlarge": {"cpu": 4, "memory": 32, "ghz": 3.1, "storage": 2500},
    "i3en.2xlarge": {"cpu": 8, "memory": 64, "ghz": 3.1, "storage": 5000},
    "i3en.3xlarge": {"cpu": 12, "memory": 96, "ghz": 3.1, "storage": 7500},
    "i3en.6xlarge": {"cpu": 24, "memory": 192, "ghz": 3.1, "storage": 15000},
    "i3en.12xlarge": {"cpu": 48, "memory": 384, "ghz": 3.1, "storage": 30000},
    "i3en.24xlarge": {"cpu": 96, "memory": 768, "ghz": 3.1, "storage": 60000},
    "i3en.metal": {"cpu": 96, "memory": 768, "ghz": 3.1, "storage": 60000},
    "inf1.xlarge": {"cpu": 4, "memory": 8, "ghz": 2.5, "storage": 0},
    "inf1.2xlarge": {"cpu": 8, "memory": 16, "ghz": 2.5, "storage": 0},
    "inf1.6xlarge": {"cpu": 24, "memory": 48, "ghz": 2.5, "storage": 0},
    "inf1.24xlarge": {"cpu": 96, "memory": 192, "ghz": 2.5, "storage": 0},
    "m1.small": {"cpu": 1, "memory": 1.7, "ghz": 0, "storage": 160},
    "m1.medium": {"cpu": 1, "memory": 3.7, "ghz": 0, "storage": 410},
    "m1.large": {"cpu": 2, "memory": 7.5, "ghz": 0, "storage": 840},
    "m1.xlarge": {"cpu": 4, "memory": 15, "ghz": 0, "storage": 1680},
    "m2.xlarge": {"cpu": 2, "memory": 17.1, "ghz": 0, "storage": 420},
    "m2.2xlarge": {"cpu": 4, "memory": 34.2, "ghz": 0, "storage": 850},
    "m2.4xlarge": {"cpu": 8, "memory": 68.4, "ghz": 0, "storage": 1680},
    "m3.medium": {"cpu": 1, "memory": 3.75, "ghz": 2.5, "storage": 4},
    "m3.large": {"cpu": 2, "memory": 7.5, "ghz": 2.5, "storage": 32},
    "m3.xlarge": {"cpu": 4, "memory": 15, "ghz": 2.5, "storage": 80},
    "m3.2xlarge": {"cpu": 8, "memory": 30, "ghz": 2.5, "storage": 160},
    "m4.large": {"cpu": 2, "memory": 8, "ghz": 2.4, "storage": 0},
    "m4.xlarge": {"cpu": 4, "memory": 16, "ghz": 2.4, "storage": 0},
    "m4.2xlarge": {"cpu": 8, "memory": 32, "ghz": 2.4, "storage": 0},
    "m4.4xlarge": {"cpu": 16, "memory": 64, "ghz": 2.4, "storage": 0},
    "m4.10xlarge": {"cpu": 40, "memory": 160, "ghz": 2.4, "storage": 0},
    "m4.16xlarge": {"cpu": 64, "memory": 256, "ghz": 2.3, "storage": 0},
    "m5.large": {"cpu": 2, "memory": 8, "ghz": 3.1, "storage": 0},
    "m5.xlarge": {"cpu": 4, "memory": 16, "ghz": 3.1, "storage": 0},
    "m5.2xlarge": {"cpu": 8, "memory": 32, "ghz": 3.1, "storage": 0},
    "m5.4xlarge": {"cpu": 16, "memory": 64, "ghz": 3.1, "storage": 0},
    "m5.8xlarge": {"cpu": 32, "memory": 128, "ghz": 3.1, "storage": 0},
    "m5.12xlarge": {"cpu": 48, "memory": 192, "ghz": 3.1, "storage": 0},
    "m5.16xlarge": {"cpu": 64, "memory": 256, "ghz": 3.1, "storage": 0},
    "m5.24xlarge": {"cpu": 96, "memory": 384, "ghz": 3.1, "storage": 0},
    "m5.metal": {"cpu": 96, "memory": 384, "ghz": 3.1, "storage": 0},
    "m5a.large": {"cpu": 2, "memory": 8, "ghz": 2.5, "storage": 0},
    "m5a.xlarge": {"cpu": 4, "memory": 16, "ghz": 2.5, "storage": 0},
    "m5a.2xlarge": {"cpu": 8, "memory": 32, "ghz": 2.5, "storage": 0},
    "m5a.4xlarge": {"cpu": 16, "memory": 64, "ghz": 2.5, "storage": 0},
    "m5a.8xlarge": {"cpu": 32, "memory": 128, "ghz": 2.5, "storage": 0},
    "m5a.12xlarge": {"cpu": 48, "memory": 192, "ghz": 2.5, "storage": 0},
    "m5a.16xlarge": {"cpu": 64, "memory": 256, "ghz": 2.5, "storage": 0},
    "m5a.24xlarge": {"cpu": 96, "memory": 384, "ghz": 2.5, "storage": 0},
    "m5ad.large": {"cpu": 2, "memory": 8, "ghz": 2.2, "storage": 75},
    "m5ad.xlarge": {"cpu": 4, "memory": 16, "ghz": 2.2, "storage": 150},
    "m5ad.2xlarge": {"cpu": 8, "memory": 32, "ghz": 2.2, "storage": 300},
    "m5ad.4xlarge": {"cpu": 16, "memory": 64, "ghz": 2.2, "storage": 600},
    "m5ad.8xlarge": {"cpu": 32, "memory": 128, "ghz": 2.5, "storage": 1200},
    "m5ad.12xlarge": {"cpu": 48, "memory": 192, "ghz": 2.2, "storage": 1800},
    "m5ad.16xlarge": {"cpu": 64, "memory": 256, "ghz": 2.5, "storage": 2400},
    "m5ad.24xlarge": {"cpu": 96, "memory": 384, "ghz": 2.2, "storage": 3600},
    "m5d.large": {"cpu": 2, "memory": 8, "ghz": 3.1, "storage": 75},
    "m5d.xlarge": {"cpu": 4, "memory": 16, "ghz": 3.1, "storage": 150},
    "m5d.2xlarge": {"cpu": 8, "memory": 32, "ghz": 3.1, "storage": 300},
    "m5d.4xlarge": {"cpu": 16, "memory": 64, "ghz": 3.1, "storage": 600},
    "m5d.8xlarge": {"cpu": 32, "memory": 128, "ghz": 3.1, "storage": 1200},
    "m5d.12xlarge": {"cpu": 48, "memory": 192, "ghz": 3.1, "storage": 1800},
    "m5d.16xlarge": {"cpu": 64, "memory": 256, "ghz": 3.1, "storage": 2400},
    "m5d.24xlarge": {"cpu": 96, "memory": 384, "ghz": 3.1, "storage": 3600},
    "m5d.metal": {"cpu": 96, "memory": 384, "ghz": 3.1, "storage": 3600},
    "m5dn.large": {"cpu": 2, "memory": 8, "ghz": 3.1, "storage": 75},
    "m5dn.xlarge": {"cpu": 4, "memory": 16, "ghz": 3.1, "storage": 150},
    "m5dn.2xlarge": {"cpu": 8, "memory": 32, "ghz": 3.1, "storage": 300},
    "m5dn.4xlarge": {"cpu": 16, "memory": 64, "ghz": 3.1, "storage": 600},
    "m5dn.8xlarge": {"cpu": 32, "memory": 128, "ghz": 3.1, "storage": 1200},
    "m5dn.12xlarge": {"cpu": 48, "memory": 192, "ghz": 3.1, "storage": 1800},
    "m5dn.16xlarge": {"cpu": 64, "memory": 256, "ghz": 3.1, "storage": 2400},
    "m5dn.24xlarge": {"cpu": 96, "memory": 384, "ghz": 3.1, "storage": 3600},
    "m5dn.metal": {"cpu": 96, "memory": 384, "ghz": 3.1, "storage": 3600},
    "m5n.large": {"cpu": 2, "memory": 8, "ghz": 3.1, "storage": 0},
    "m5n.xlarge": {"cpu": 4, "memory": 16, "ghz": 3.1, "storage": 0},
    "m5n.2xlarge": {"cpu": 8, "memory": 32, "ghz": 3.1, "storage": 0},
    "m5n.4xlarge": {"cpu": 16, "memory": 64, "ghz": 3.1, "storage": 0},
    "m5n.8xlarge": {"cpu": 32, "memory": 128, "ghz": 3.1, "storage": 0},
    "m5n.12xlarge": {"cpu": 48, "memory": 192, "ghz": 3.1, "storage": 0},
    "m5n.16xlarge": {"cpu": 64, "memory": 256, "ghz": 3.1, "storage": 0},
    "m5n.24xlarge": {"cpu": 96, "memory": 384, "ghz": 3.1, "storage": 0},
    "m5n.metal": {"cpu": 96, "memory": 384, "ghz": 3.1, "storage": 0},
    "m5zn.large": {"cpu": 2, "memory": 8, "ghz": 4.5, "storage": 0},
    "m5zn.xlarge": {"cpu": 4, "memory": 16, "ghz": 4.5, "storage": 0},
    "m5zn.2xlarge": {"cpu": 8, "memory": 32, "ghz": 4.5, "storage": 0},
    "m5zn.3xlarge": {"cpu": 12, "memory": 48, "ghz": 4.5, "storage": 0},
    "m5zn.6xlarge": {"cpu": 24, "memory": 96, "ghz": 4.5, "storage": 0},
    "m5zn.12xlarge": {"cpu": 48, "memory": 192, "ghz": 4.5, "storage": 0},
    "m5zn.metal": {"cpu": 48, "memory": 192, "ghz": 4.5, "storage": 0},
    "m6g.medium": {"cpu": 1, "memory": 4, "ghz": 2.5, "storage": 0},
    "m6g.large": {"cpu": 2, "memory": 8, "ghz": 2.5, "storage": 0},
    "m6g.xlarge": {"cpu": 4, "memory": 16, "ghz": 2.5, "storage": 0},
    "m6g.2xlarge": {"cpu": 8, "memory": 32, "ghz": 2.5, "storage": 0},
    "m6g.4xlarge": {"cpu": 16, "memory": 64, "ghz": 2.5, "storage": 0},
    "m6g.8xlarge": {"cpu": 32, "memory": 128, "ghz": 2.5, "storage": 0},
    "m6g.12xlarge": {"cpu": 48, "memory": 192, "ghz": 2.5, "storage": 0},
    "m6g.16xlarge": {"cpu": 64, "memory": 256, "ghz": 2.5, "storage": 0},
    "m6g.metal": {"cpu": 64, "memory": 256, "ghz": 2.5, "storage": 0},
    "m6gd.medium": {"cpu": 1, "memory": 4, "ghz": 2.5, "storage": 59},
    "m6gd.large": {"cpu": 2, "memory": 8, "ghz": 2.5, "storage": 118},
    "m6gd.xlarge": {"cpu": 4, "memory": 16, "ghz": 2.5, "storage": 237},
    "m6gd.2xlarge": {"cpu": 8, "memory": 32, "ghz": 2.5, "storage": 474},
    "m6gd.4xlarge": {"cpu": 16, "memory": 64, "ghz": 2.5, "storage": 950},
    "m6gd.8xlarge": {"cpu": 32, "memory": 128, "ghz": 2.5, "storage": 1900},
    "m6gd.12xlarge": {"cpu": 48, "memory": 192, "ghz": 2.5, "storage": 2850},
    "m6gd.16xlarge": {"cpu": 64, "memory": 256, "ghz": 2.5, "storage": 3800},
    "m6gd.metal": {"cpu": 64, "memory": 256, "ghz": 2.5, "storage": 3800},
    "mac1.metal": {"cpu": 12, "memory": 32, "ghz": 3.2, "storage": 0},
    "p2.xlarge": {"cpu": 4, "memory": 61, "ghz": 2.7, "storage": 0},
    "p2.8xlarge": {"cpu": 32, "memory": 488, "ghz": 2.7, "storage": 0},
    "p2.16xlarge": {"cpu": 64, "memory": 732, "ghz": 2.3, "storage": 0},
    "p3.2xlarge": {"cpu": 8, "memory": 61, "ghz": 2.7, "storage": 0},
    "p3.8xlarge": {"cpu": 32, "memory": 244, "ghz": 2.7, "storage": 0},
    "p3.16xlarge": {"cpu": 64, "memory": 488, "ghz": 2.7, "storage": 0},
    "p3dn.24xlarge": {"cpu": 96, "memory": 768, "ghz": 2.5, "storage": 1800},
    "p4d.24xlarge": {"cpu": 96, "memory": 1152, "ghz": 3, "storage": 8000},
    "r3.large": {"cpu": 2, "memory": 15, "ghz": 2.5, "storage": 32},
    "r3.xlarge": {"cpu": 4, "memory": 30.5, "ghz": 2.5, "storage": 80},
    "r3.2xlarge": {"cpu": 8, "memory": 61, "ghz": 2.5, "storage": 160},
    "r3.4xlarge": {"cpu": 16, "memory": 122, "ghz": 2.5, "storage": 320},
    "r3.8xlarge": {"cpu": 32, "memory": 244, "ghz": 2.5, "storage": 640},
    "r4.large": {"cpu": 2, "memory": 15.3, "ghz": 2.3, "storage": 0},
    "r4.xlarge": {"cpu": 4, "memory": 30.5, "ghz": 2.3, "storage": 0},
    "r4.2xlarge": {"cpu": 8, "memory": 61, "ghz": 2.3, "storage": 0},
    "r4.4xlarge": {"cpu": 16, "memory": 122, "ghz": 2.3, "storage": 0},
    "r4.8xlarge": {"cpu": 32, "memory": 244, "ghz": 2.3, "storage": 0},
    "r4.16xlarge": {"cpu": 64, "memory": 488, "ghz": 2.3, "storage": 0},
    "r5.large": {"cpu": 2, "memory": 16, "ghz": 3.1, "storage": 0},
    "r5.xlarge": {"cpu": 4, "memory": 32, "ghz": 3.1, "storage": 0},
    "r5.2xlarge": {"cpu": 8, "memory": 64, "ghz": 3.1, "storage": 0},
    "r5.4xlarge": {"cpu": 16, "memory": 128, "ghz": 3.1, "storage": 0},
    "r5.8xlarge": {"cpu": 32, "memory": 256, "ghz": 3.1, "storage": 0},
    "r5.12xlarge": {"cpu": 48, "memory": 384, "ghz": 3.1, "storage": 0},
    "r5.16xlarge": {"cpu": 64, "memory": 512, "ghz": 3.1, "storage": 0},
    "r5.24xlarge": {"cpu": 96, "memory": 768, "ghz": 3.1, "storage": 0},
    "r5.metal": {"cpu": 96, "memory": 768, "ghz": 3.1, "storage": 0},
    "r5a.large": {"cpu": 2, "memory": 16, "ghz": 2.5, "storage": 0},
    "r5a.xlarge": {"cpu": 4, "memory": 32, "ghz": 2.5, "storage": 0},
    "r5a.2xlarge": {"cpu": 8, "memory": 64, "ghz": 2.5, "storage": 0},
    "r5a.4xlarge": {"cpu": 16, "memory": 128, "ghz": 2.5, "storage": 0},
    "r5a.8xlarge": {"cpu": 32, "memory": 256, "ghz": 2.5, "storage": 0},
    "r5a.12xlarge": {"cpu": 48, "memory": 384, "ghz": 2.5, "storage": 0},
    "r5a.16xlarge": {"cpu": 64, "memory": 512, "ghz": 2.5, "storage": 0},
    "r5a.24xlarge": {"cpu": 96, "memory": 768, "ghz": 2.5, "storage": 0},
    "r5ad.large": {"cpu": 2, "memory": 16, "ghz": 2.2, "storage": 75},
    "r5ad.xlarge": {"cpu": 4, "memory": 32, "ghz": 2.2, "storage": 150},
    "r5ad.2xlarge": {"cpu": 8, "memory": 64, "ghz": 2.2, "storage": 300},
    "r5ad.4xlarge": {"cpu": 16, "memory": 128, "ghz": 2.2, "storage": 600},
    "r5ad.8xlarge": {"cpu": 32, "memory": 256, "ghz": 2.5, "storage": 1200},
    "r5ad.12xlarge": {"cpu": 48, "memory": 384, "ghz": 2.2, "storage": 1800},
    "r5ad.16xlarge": {"cpu": 64, "memory": 512, "ghz": 2.5, "storage": 2400},
    "r5ad.24xlarge": {"cpu": 96, "memory": 768, "ghz": 2.2, "storage": 3600},
    "r5b.large": {"cpu": 2, "memory": 16, "ghz": 3.1, "storage": 0},
    "r5b.xlarge": {"cpu": 4, "memory": 32, "ghz": 3.1, "storage": 0},
    "r5b.2xlarge": {"cpu": 8, "memory": 64, "ghz": 3.1, "storage": 0},
    "r5b.4xlarge": {"cpu": 16, "memory": 128, "ghz": 3.1, "storage": 0},
    "r5b.8xlarge": {"cpu": 32, "memory": 256, "ghz": 3.1, "storage": 0},
    "r5b.12xlarge": {"cpu": 48, "memory": 384, "ghz": 3.1, "storage": 0},
    "r5b.16xlarge": {"cpu": 64, "memory": 512, "ghz": 3.1, "storage": 0},
    "r5b.24xlarge": {"cpu": 96, "memory": 768, "ghz": 3.1, "storage": 0},
    "r5b.metal": {"cpu": 96, "memory": 768, "ghz": 3.1, "storage": 0},
    "r5d.large": {"cpu": 2, "memory": 16, "ghz": 3.1, "storage": 75},
    "r5d.xlarge": {"cpu": 4, "memory": 32, "ghz": 3.1, "storage": 150},
    "r5d.2xlarge": {"cpu": 8, "memory": 64, "ghz": 3.1, "storage": 300},
    "r5d.4xlarge": {"cpu": 16, "memory": 128, "ghz": 3.1, "storage": 600},
    "r5d.8xlarge": {"cpu": 32, "memory": 256, "ghz": 3.1, "storage": 1200},
    "r5d.12xlarge": {"cpu": 48, "memory": 384, "ghz": 3.1, "storage": 1800},
    "r5d.16xlarge": {"cpu": 64, "memory": 512, "ghz": 3.1, "storage": 2400},
    "r5d.24xlarge": {"cpu": 96, "memory": 768, "ghz": 3.1, "storage": 3600},
    "r5d.metal": {"cpu": 96, "memory": 768, "ghz": 3.1, "storage": 3600},
    "r5dn.large": {"cpu": 2, "memory": 16, "ghz": 3.1, "storage": 75},
    "r5dn.xlarge": {"cpu": 4, "memory": 32, "ghz": 3.1, "storage": 150},
    "r5dn.2xlarge": {"cpu": 8, "memory": 64, "ghz": 3.1, "storage": 300},
    "r5dn.4xlarge": {"cpu": 16, "memory": 128, "ghz": 3.1, "storage": 600},
    "r5dn.8xlarge": {"cpu": 32, "memory": 256, "ghz": 3.1, "storage": 1200},
    "r5dn.12xlarge": {"cpu": 48, "memory": 384, "ghz": 3.1, "storage": 1800},
    "r5dn.16xlarge": {"cpu": 64, "memory": 512, "ghz": 3.1, "storage": 2400},
    "r5dn.24xlarge": {"cpu": 96, "memory": 768, "ghz": 3.1, "storage": 3600},
    "r5dn.metal": {"cpu": 96, "memory": 768, "ghz": 3.1, "storage": 3600},
    "r5n.large": {"cpu": 2, "memory": 16, "ghz": 3.1, "storage": 0},
    "r5n.xlarge": {"cpu": 4, "memory": 32, "ghz": 3.1, "storage": 0},
    "r5n.2xlarge": {"cpu": 8, "memory": 64, "ghz": 3.1, "storage": 0},
    "r5n.4xlarge": {"cpu": 16, "memory": 128, "ghz": 3.1, "storage": 0},
    "r5n.8xlarge": {"cpu": 32, "memory": 256, "ghz": 3.1, "storage": 0},
    "r5n.12xlarge": {"cpu": 48, "memory": 384, "ghz": 3.1, "storage": 0},
    "r5n.16xlarge": {"cpu": 64, "memory": 512, "ghz": 3.1, "storage": 0},
    "r5n.24xlarge": {"cpu": 96, "memory": 768, "ghz": 3.1, "storage": 0},
    "r5n.metal": {"cpu": 96, "memory": 768, "ghz": 3.1, "storage": 0},
    "r6g.medium": {"cpu": 1, "memory": 8, "ghz": 2.5, "storage": 0},
    "r6g.large": {"cpu": 2, "memory": 16, "ghz": 2.5, "storage": 0},
    "r6g.xlarge": {"cpu": 4, "memory": 32, "ghz": 2.5, "storage": 0},
    "r6g.2xlarge": {"cpu": 8, "memory": 64, "ghz": 2.5, "storage": 0},
    "r6g.4xlarge": {"cpu": 16, "memory": 128, "ghz": 2.5, "storage": 0},
    "r6g.8xlarge": {"cpu": 32, "memory": 256, "ghz": 2.5, "storage": 0},
    "r6g.12xlarge": {"cpu": 48, "memory": 384, "ghz": 2.5, "storage": 0},
    "r6g.16xlarge": {"cpu": 64, "memory": 512, "ghz": 2.5, "storage": 0},
    "r6g.metal": {"cpu": 64, "memory": 512, "ghz": 2.5, "storage": 0},
    "r6gd.medium": {"cpu": 1, "memory": 8, "ghz": 2.5, "storage": 59},
    "r6gd.large": {"cpu": 2, "memory": 16, "ghz": 2.5, "storage": 118},
    "r6gd.xlarge": {"cpu": 4, "memory": 32, "ghz": 2.5, "storage": 237},
    "r6gd.2xlarge": {"cpu": 8, "memory": 64, "ghz": 2.5, "storage": 474},
    "r6gd.4xlarge": {"cpu": 16, "memory": 128, "ghz": 2.5, "storage": 950},
    "r6gd.8xlarge": {"cpu": 32, "memory": 256, "ghz": 2.5, "storage": 1900},
    "r6gd.12xlarge": {"cpu": 48, "memory": 384, "ghz": 2.5, "storage": 2850},
    "r6gd.16xlarge": {"cpu": 64, "memory": 512, "ghz": 2.5, "storage": 3800},
    "r6gd.metal": {"cpu": 64, "memory": 512, "ghz": 2.5, "storage": 3800},
    "t3a.nano": {"cpu": 2, "memory": 0.5, "ghz": 2.2, "storage": 0},
    "t3a.micro": {"cpu": 2, "memory": 1, "ghz": 2.2, "storage": 0},
    "t3a.small": {"cpu": 2, "memory": 2, "ghz": 2.2, "storage": 0},
    "t3a.medium": {"cpu": 2, "memory": 4, "ghz": 2.2, "storage": 0},
    "t3a.large": {"cpu": 2, "memory": 8, "ghz": 2.2, "storage": 0},
    "t3a.xlarge": {"cpu": 4, "memory": 16, "ghz": 2.2, "storage": 0},
    "t3a.2xlarge": {"cpu": 8, "memory": 32, "ghz": 2.2, "storage": 0},
    "t4g.nano": {"cpu": 2, "memory": 0.5, "ghz": 2.5, "storage": 0},
    "t4g.micro": {"cpu": 2, "memory": 1, "ghz": 2.5, "storage": 0},
    "t4g.small": {"cpu": 2, "memory": 2, "ghz": 2.5, "storage": 0},
    "t4g.medium": {"cpu": 2, "memory": 4, "ghz": 2.5, "storage": 0},
    "t4g.large": {"cpu": 2, "memory": 8, "ghz": 2.5, "storage": 0},
    "t4g.xlarge": {"cpu": 4, "memory": 16, "ghz": 2.5, "storage": 0},
    "t4g.2xlarge": {"cpu": 8, "memory": 32, "ghz": 2.5, "storage": 0},
    "x1.16xlarge": {"cpu": 64, "memory": 976, "ghz": 2.3, "storage": 1920},
    "x1.32xlarge": {"cpu": 128, "memory": 1952, "ghz": 2.3, "storage": 3840},
    "x1e.xlarge": {"cpu": 4, "memory": 122, "ghz": 2.3, "storage": 120},
    "x1e.2xlarge": {"cpu": 8, "memory": 244, "ghz": 2.3, "storage": 240},
    "x1e.4xlarge": {"cpu": 16, "memory": 488, "ghz": 2.3, "storage": 480},
    "x1e.8xlarge": {"cpu": 32, "memory": 976, "ghz": 2.3, "storage": 960},
    "x1e.16xlarge": {"cpu": 64, "memory": 1952, "ghz": 2.3, "storage": 1920},
    "x1e.32xlarge": {"cpu": 128, "memory": 3904, "ghz": 2.3, "storage": 3840},
    "x2gd.medium": {"cpu": 1, "memory": 16, "ghz": 2.5, "storage": 59},
    "x2gd.large": {"cpu": 2, "memory": 32, "ghz": 2.5, "storage": 118},
    "x2gd.xlarge": {"cpu": 4, "memory": 64, "ghz": 2.5, "storage": 237},
    "x2gd.2xlarge": {"cpu": 8, "memory": 128, "ghz": 2.5, "storage": 475},
    "x2gd.4xlarge": {"cpu": 16, "memory": 256, "ghz": 2.5, "storage": 950},
    "x2gd.8xlarge": {"cpu": 32, "memory": 512, "ghz": 2.5, "storage": 1900},
    "x2gd.12xlarge": {"cpu": 48, "memory": 768, "ghz": 2.5, "storage": 2850},
    "x2gd.16xlarge": {"cpu": 64, "memory": 1024, "ghz": 2.5, "storage": 3800},
    "x2gd.metal": {"cpu": 64, "memory": 1024, "ghz": 2.5, "storage": 3800},
    "z1d.large": {"cpu": 2, "memory": 16, "ghz": 4, "storage": 75},
    "z1d.xlarge": {"cpu": 4, "memory": 32, "ghz": 4, "storage": 150},
    "z1d.2xlarge": {"cpu": 8, "memory": 64, "ghz": 4, "storage": 300},
    "z1d.3xlarge": {"cpu": 12, "memory": 96, "ghz": 4, "storage": 450},
    "z1d.6xlarge": {"cpu": 24, "memory": 192, "ghz": 4, "storage": 900},
    "z1d.12xlarge": {"cpu": 48, "memory": 384, "ghz": 4, "storage": 1800},
    "z1d.metal": {"cpu": 48, "memory": 384, "ghz": 4, "storage": 1800}
}
