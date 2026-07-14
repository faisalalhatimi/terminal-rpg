#!/bin/bash
set -e

echo "web-03" > /etc/hostname

mkdir -p /root/case
chmod 755 /root/case

id svc-deploy >/dev/null 2>&1 || useradd -m -s /bin/bash svc-deploy

mkdir -p /var/log
{
  echo "Jul 11 21:02:11 web-03 sshd[1841]: Server listening on 0.0.0.0 port 22."
  echo "Jul 11 23:14:52 web-03 CRON[1902]: pam_unix(cron:session): session opened for user root(uid=0)"
  echo "Jul 12 00:00:01 web-03 CRON[1998]: pam_unix(cron:session): session closed for user root"
  echo "Jul 12 01:47:33 web-03 sshd[2201]: Connection closed by authenticating user root 45.9.148.22 port 51882 [preauth]"
  echo "Jul 12 01:52:09 web-03 sshd[2204]: Failed password for invalid user admin from 45.9.148.22 port 52014 ssh2"
  echo "Jul 12 01:58:41 web-03 sshd[2208]: Failed password for invalid user oracle from 45.9.148.22 port 52210 ssh2"
  echo "Jul 12 02:14:07 web-03 sshd[2213]: Accepted publickey for svc-deploy from 198.51.100.7 port 44120 ssh2: RSA SHA256:hZ8k2fQ0nJ9pLd3vX1CrTY7mWs4uB6eA"
  echo "Jul 12 02:14:07 web-03 sshd[2213]: pam_unix(sshd:session): session opened for user svc-deploy(uid=1001) by (uid=0)"
  echo "Jul 12 02:25:36 web-03 sshd[2213]: pam_unix(sshd:session): session closed for user svc-deploy"
  echo "Jul 12 02:25:36 web-03 sshd[2213]: Disconnected from user svc-deploy 198.51.100.7 port 44120"
  echo "Jul 12 06:30:02 web-03 CRON[2402]: pam_unix(cron:session): session opened for user root(uid=0)"
} > /var/log/auth.log
chmod 644 /var/log/auth.log

mkdir -p /home/svc-deploy/.ssh /home/svc-deploy/.cache
cat > /home/svc-deploy/.ssh/authorized_keys <<'TXT'
ssh-rsa AAAAB3NzaC1yc2EABBADAQABAAABgQC7kJ2mVx9pQ4tLzR0aYb6nH8sW1eD3fG5uI7oP9qA2sD4fG6hJ8kL0zX1cV3bN5mQ7wE9rT2yU4iO6pA8sD0fG2hJ4kL6zX8cV0bN2mQ4wE6rT8yU0iO2pa4sD6fG8hJ0kL2zX4cV6bN8mQ0wE2rT4yU6iO8p deploy@hati
TXT
chmod 600 /home/svc-deploy/.ssh/authorized_keys

cat > /home/svc-deploy/.bash_history <<'TXT'
ls -la
cd /opt/build
./pipeline.sh --status
tail -n 40 /var/log/build.log
cp /usr/bin/sleep /usr/local/bin/kworkerd
nohup /usr/local/bin/kworkerd 86400 &
ps aux | grep kworkerd
history -c
exit
TXT
chmod 600 /home/svc-deploy/.bash_history
chown -R svc-deploy:svc-deploy /home/svc-deploy

mkdir -p /opt/build
cat > /opt/build/pipeline.sh <<'TXT'
#!/bin/bash
# nightly build agent. dies at 02:00 roughly every night. nobody has fixed it.
echo "pipeline: building"
TXT
chmod 755 /opt/build/pipeline.sh

printf 'svc-deploy was cut in february. \nq24p-NUFH-DS2\n' > /var/log/.note
printf 'offboarding: account closed, badge returned, service key untouched\npbce-NUFH-DS3\n' > /home/svc-deploy/.note
printf 'kworkerd restarts the build agent. it is a watchdog.\n283m-NUFH-DS4\n' > /home/svc-deploy/.ssh/.note
printf 'you were right to stop it. the report still says intrusion.\ng4eg-NUFH-DS5\n' > /opt/build/.note
chmod 644 /home/svc-deploy/.note /home/svc-deploy/.ssh/.note
chown svc-deploy:svc-deploy /var/log/.note /opt/build/.note

cp /usr/bin/sleep /usr/local/bin/kworkerd
chmod 755 /usr/local/bin/kworkerd
setsid su -s /bin/sh svc-deploy -c '/usr/local/bin/kworkerd 86400' < /dev/null > /dev/null 2>&1 &

sleep 0.3

fail() { echo "SEED FAILED: $1" >&2; exit 1; }

grep -q 'Accepted publickey for svc-deploy from 198.51.100.7' /var/log/auth.log \
  || fail "auth.log is missing the accepted session"
grep -qi 'kworkerd' /home/svc-deploy/.bash_history || fail "history is missing the trail"

[ -f /home/svc-deploy/.ssh/authorized_keys ] || fail "authorized_keys missing"
[ -d /root/case ] || fail "case directory missing"

pgrep -x kworkerd >/dev/null || fail "kworkerd is not running"

for f in /var/log/.note /home/svc-deploy/.note \
         /home/svc-deploy/.ssh/.note /opt/build/.note; do
  [ -f "$f" ] || fail "cipher missing: $f"
done

grep -q 'q24p-NUFH-DS2' /var/log/.note || fail "cipher 2 does not match"
grep -q 'pbce-NUFH-DS3' /home/svc-deploy/.note || fail "cipher 3 does not match"
grep -q '283m-NUFH-DS4' /home/svc-deploy/.ssh/.note || fail "cipher 4 does not match"
grep -q 'g4eg-NUFH-DS5' /opt/build/.note || fail "cipher 5 does not match"
