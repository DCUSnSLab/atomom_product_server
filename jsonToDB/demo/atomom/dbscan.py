import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import cv2
from sklearn.cluster import DBSCAN


# Define a function to generate clusters
def cluster_gen(n_clusters, pts_minmax=(10, 100), x_mult=(1, 4), y_mult=(1, 3),
                x_off=(0, 50), y_off=(0, 50)):
    # n_clusters = number of clusters to generate
    # pts_minmax = range of number of points per cluster
    # x_mult = range of multiplier to modify the size of cluster in the x-direction
    # y_mult = range of multiplier to modify the size of cluster in the x-direction
    # x_off = range of cluster position offset in the x-direction
    # y_off = range of cluster position offset in the y-direction

    # Initialize some empty lists to receive cluster member positions
    clusters_x = []
    clusters_y = []
    # Genereate random values given parameter ranges
    n_points = np.random.randint(pts_minmax[0], pts_minmax[1], n_clusters)
    x_multipliers = np.random.randint(x_mult[0], x_mult[1], n_clusters)
    y_multipliers = np.random.randint(y_mult[0], y_mult[1], n_clusters)
    x_offsets = np.random.randint(x_off[0], x_off[1], n_clusters)
    y_offsets = np.random.randint(y_off[0], y_off[1], n_clusters)

    # Generate random clusters given parameter values
    for idx, npts in enumerate(n_points):
        xpts = np.random.randn(npts) * x_multipliers[idx] + x_offsets[idx]
        ypts = np.random.randn(npts) * y_multipliers[idx] + y_offsets[idx]
        clusters_x.append(xpts)
        clusters_y.append(ypts)

    # Return cluster positions
    return clusters_x, clusters_y

def customDBscan_vis_True():
    pass
def customDBscan_vis_False():
    pass

def customDBscan(data,rows,cols,eps,minPts):
    db = DBSCAN(eps=eps, min_samples=minPts).fit(data)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    unique_labels = set(labels)

    fig = plt.figure(figsize=(12, 6))
    plt.subplot(131)
    plt.plot(data[:, 0], data[:, 1], 'ko')
    plt.xlim(0, cols)
    plt.ylim(0, rows)
    ax = plt.gca()
    ax.set_ylim(ax.get_ylim()[::-1])
    plt.title('Original Data', fontsize=20)

    plt.subplot(132)
    # The following is just a fancy way of plotting core, edge and outliers
    # Credit to: http://scikit-learn.org/stable/auto_examples/cluster/plot_dbscan.html#sphx-glr-auto-examples-cluster-plot-dbscan-py
    colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]

    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_member_mask = (labels == k)

        xy = data[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='none',markersize=7)


        # xy = data[class_member_mask & ~core_samples_mask]
        # plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
        #           markeredgecolor='none',markersize=3)
    plt.xlim(0, cols)
    plt.ylim(0, rows)
    plt.title('DBSCAN: %d clusters found' % n_clusters, fontsize=20)
    fig.tight_layout()
    plt.subplots_adjust(left=0.03, right=0.98, top=0.9, bottom=0.05)
    ax = plt.gca()
    ax.set_ylim(ax.get_ylim()[::-1])

    plt.show()

def run(img,bboxs,eps,minPts,vis=False):
    zeros = np.zeros((rows, cols), dtype=np.uint8)
    for i in bboxs:
        y1,x1,y2,x2=i
        cv2.rectangle(zeros, (x1, y1), (x2, y2), (255, 0, 0), 1)
    cum = []
    x, y = np.where(zeros == 255)
    for i, data in enumerate(x):
        zeros[x[i],y[i]]=255
        cum.append([y[i],x[i]])
    if(vis==True):
        # cv2.namedWindow("img", cv2.WINDOW_NORMAL)
        # cv2.namedWindow("img2", cv2.WINDOW_NORMAL)
        # cv2.namedWindow("img3", cv2.WINDOW_NORMAL)
        # cv2.resizeWindow("img", width=640, height=480)
        # cv2.resizeWindow("img2", width=640, height=480)
        # cv2.resizeWindow("img3", width=640, height=480)
        # cv2.imshow("img", img)
        customDBscan(np.array(cum), rows=rows, cols=cols, eps=eps, minPts=minPts)
        # cv2.waitKey(0)
        pass
if __name__ == '__main__':
    img = cv2.imread("../../../demo_image/39.jpg")
    bboxs = np.load('C:/Users/dgdgk/Documents/nps/bbox3.npy')
    rows,cols,_=img.shape

    eps=25
    minPts=2

    run(img=img,bboxs=bboxs,eps=eps,minPts=minPts,vis=True)



