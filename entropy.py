import math
class Entropy():
	def __init__(self,):
		self.threshold=float(2)
		self.W=500
		self.entropy_list=[]
		self.init()
		self.ddos=int(0)
	def init(self):
		self.src=[]
		self.dst=[]
		self.pkt={}
		self.count=0
	def get_stat(self,src_ip,dst_ip,packet_num):
		self.count+=1		
		self.src.append(src_ip)
		self.dst.append(dst_ip)
		if self.count==self.W:
			for ip in self.src:
				if ip not in self.pkt:
					self.pkt[ip]=0
				self.pkt[ip] += 1
			if(self.cal_entropy()>self.threshold):
				print('entropy > threshold\n')
				self.ddos+=1
			else: 	
				self.ddos=max(0,self.ddos-1)
			if(self.ddos>=3):
				return True
			self.init()
		return False
	def cal_entropy(self):
		entropy=0
		l=len(self.src)
		#print("len=",l)
		for i,n in self.pkt.items():
			prob = n/float(l)
			#print(i,n)
			entropy += (-prob* math.log(prob,10))
		print("entropy=",entropy)
		self.entropy_list.append(entropy)
		return entropy

