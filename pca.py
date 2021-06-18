import numpy as np 
import scipy.stats as sps
import matplotlib.pyplot as plt

class PCA():
    # Initialize PCA object
    def __init__(
        self, 
        time_dim, 
        num_link
    ):
        self.data = np.empty([time_dim,num_link], dtype=float)
        self.time_dim = time_dim
        self.num_link = num_link
        self.num_element = 0

    # Update data in first "time_dim" time sliced
    def init_data_matrix(
        self,
        data,   # Should be a list with number of links element
        index,  # 0 <= index < time_dim
    ): 
        assert 0 <= index and index < self.time_dim and len(data) == self.num_link
        row_data = np.array(data)
        self.data[index,:] = row_data[:]
        self.num_element += 1 

    # Updata data after first "time_dim" time sliced
    def update_data(
        self, 
        data,  # Should be a list with number of links element
    ):
        assert len(data) == self.num_link
        row_data = np.array(data).reshape(1,-1)
        self.data = np.concatenate((self.data[1:,:], row_data[:,:]),axis=0)

    # Compute eigenvalues and eigenvectors
    def compute_eigen(
        self,
    ):
        x_mean = np.mean(self.data, axis=0)
        X = self.data-x_mean
        cov_X = np.dot(X.T, X) / self.time_dim
        eigenvalues, eigenvectors = np.linalg.eig(cov_X)
        return eigenvalues, eigenvectors

    # Compute the value of "r" mentioned in paper
    def compute_r(
        self, 
        eigenvectors,
    ):
        for r in range(len(eigenvectors)):
            proj = np.dot(self.data, eigenvectors[r])
            avg_proj = np.mean(proj)
            std_proj = np.std(proj)
            for value in proj: 
                if value < avg_proj - 3*std_proj or value > avg_proj + 3*std_proj:
                    return r 
        # In this case, every eigenvectors is treated as a coloum of P. Anomaly subspace is empty. 
        return len(eigenvectors) 

    # Compute the value of "delta" mentioned in paper
    def compute_delta(
        self, 
        eigenvalues,  # The eigenvalues in range r+1 to number of links 
    ):
        phi_1 = np.sum(eigenvalues)
        phi_2 = np.sum(eigenvalues**2)
        phi_3 = np.sum(eigenvalues**3)  
        # When phi_1 = 0, it is obvious that phi_2, phi_3, and h_0(can be calculated by limit) are also 0
        # The final equation when phi_1, phi_2, phi_3, and h_0 goes to 0 will be equal to 0, too. 
        if phi_1 == 0:
            return 0
        h_0 = 1 - (2*phi_1*phi_3)/(3*(phi_2**2))
        # Compute the 1− α percentile in a standard normal distribution.
        alpha = 0.005
        dist = sps.norm(loc=0, scale=1)
        c_alpha = dist.ppf(1-alpha)
        return phi_1 * (((c_alpha*((2*phi_2*(h_0**2))**(1/2))/phi_1)+1+(phi_2*h_0*(h_0-1)/(phi_1**2)))**(1/h_0))

    # Detect DDOS
    def detect_ddos(
        self, 
    ):  
        assert self.num_element == self.time_dim   
        x = self.data[self.time_dim-1,:]
        eigenvalues, eigenvectors = self.compute_eigen()
        r = self.compute_r(eigenvectors)
        if r == self.num_link:
            return False, None
        P = eigenvectors[:r,:].T 
        x_normal = np.dot(np.dot(P,P.T),x)
        x_abnormal = np.dot(np.identity(P.shape[0])-np.dot(P,P.T),x)
        SPE = np.linalg.norm(x_abnormal)**2
        delta = self.compute_delta(eigenvalues[r:])
        if SPE <= delta:
            return False, x_abnormal
        else:
            return True, x_abnormal

