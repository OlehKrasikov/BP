import numpy as np
from PIL import Image
import time


def rand_init_membership_matrix(width, height):
    mm = np.random.rand(width, height)
    mm = mm / mm.sum(axis=1, keepdims=True)
    return mm

def calc_distance(data, centers, color_coefficient, width=None, height=None):

    matrix_of_distance = np.zeros((data.shape[0], centers.shape[0]))

    norm_for_pixel_dist = np.sqrt(width ** 2 + height ** 2)
    for x in range(centers.shape[0]):
        center = centers[x]

        color_dist = np.sqrt(np.sum((data[:, :3] - center[:3]) ** 2, axis=1)) / 255

        pixel_dist = np.sqrt(np.sum((data[:, 3:] - center[3:]) ** 2, axis=1)) / norm_for_pixel_dist

        matrix_of_distance[:, x] = color_coefficient * color_dist + (1 - color_coefficient) * pixel_dist
    return matrix_of_distance


def membership_matrix_calc(n_clusters, centers, m, data,coef,height,width):
    dist = calc_distance(data, centers, coef, width, height)
    
    dist = np.fmax(dist, 1e-12)
    
    power = 2.0 / (m - 1.0)
    
    temp = dist[:, :, np.newaxis] / dist[:, np.newaxis, :]
    temp = temp ** power
    
    membership_matrix = 1.0 / np.sum(temp, axis=2)
    
    return membership_matrix


def new_clusters_centers_calc(n_clusters, membership_matrix, data, m):
    new_centers = np.zeros((n_clusters,5))

    for i in range(n_clusters):
        buffer = ((membership_matrix[:,i]) ** m)
        for j in range(5):
            numerator = np.sum(data[:,j] * buffer)
            denominator = np.sum(buffer)
            new_centers[i][j] = numerator / denominator
    return new_centers


def fcm(n_clusters, m, data, max_iterations, E, color_coefficient,height,width):
    start_time = time.time()
    n_points = data.shape[0]
    i = 0
    old_mm = np.zeros((n_points, n_clusters))
    clusters_centers = np.zeros((n_clusters, data.shape[1]))
    mm = rand_init_membership_matrix(n_points, n_clusters)
    while 1:
        if i > 0:
            if np.max(np.abs(mm - old_mm)) < E:
                print('dosiahnutá požadovaná presnosť', '\n', 'i = ', i)

                break
            elif i > max_iterations:
                print('dosiahnutý limit iterácií i = ', i,'\n','presnosť:',np.max(np.abs(mm - old_mm)))
                break
        clusters_centers = new_clusters_centers_calc(n_clusters, mm, data, m)
        old_mm = np.array(mm)
        mm = membership_matrix_calc(n_clusters, clusters_centers, m, data,color_coefficient,height,width)
        i += 1

    end_time = time.time()
    print("čas vykonania: {:.4f} sekund".format(end_time - start_time))
    return clusters_centers, mm


def cluster_image(membership_matrix, n_clusters):
    n_points = membership_matrix.shape[0]
    output = np.zeros((n_points, 3), dtype=np.uint8)
    colors = np.array([
        [255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0],
        [255, 0, 255], [0, 255, 255], [255, 128, 0], [128, 0, 255]
    ])
    binary = np.array([
        [255,255,255],[0,0,0]
    ])
    
    if n_clusters <= 2:
        for i in range(n_points):
            cluster_idx = np.argmax(membership_matrix[i])
            
            output[i] = binary[cluster_idx % len(binary)]
    else:
        for i in range(n_points):
            cluster_idx = np.argmax(membership_matrix[i])
            
            output[i] = colors[cluster_idx % len(colors)]
    return output


#####################################################################################

 
