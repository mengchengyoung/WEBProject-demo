import os 
import tempfile
from celery import task
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header

@task
def Generatebam(region, bamfile, bamfile_out, tempPath=tempfile.gettempdir()):
    temp_bed = os.path.join(tempPath, 'temp.bed')
    time_suffix = time.strftime("%Y%m%d%M%S", time.localtime(time.time()))
    temp_bam = os.path.join(tempPath, 'temp_{}.bam'.format(time_suffix))
    #print(bamfile, temp_bed, temp_bam)
    with open(temp_bed, 'w') as f:
        f.write("{}\t{}\t{}".format(region[0], region[1], region[2]))

    command = "samtools view {bamfile} -L {tempbed} -b -o {tempbam}".format(bamfile = bamfile,
                                                                            tempbed = temp_bed,
                                                                            tempbam = bamfile_out) 
    os.system(command) 


@task
def merge_vcf(vcf1, vcf2, vcf):
    os.system('cat {} {} >{}'.format(vcf1, vcf2, vcf))

@task 
def mail_warn(sample):
    mail_host = os.environ['mail_host']
    mail_user = os.environ['mail_user']
    mail_pass = os.environ['mail_pass']
    mail_port = os.environ['mail_port']
    receivers = ['mengchengyang@annoroad.com']
    sender = 'leukemia@annoroad.com'
    message = MIMEText('{} 校验出错，手动校验...'.format(sample), 'plain', 'utf-8')

    message['From'] = sender
    message['To'] = receivers
    message['Subject'] = '顺反式校验出错'
    smtpObj = smtplib.SMTP() 
    smtpObj.connect(mail_host, mail_port)
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
        


