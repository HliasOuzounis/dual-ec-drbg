import matplotlib.pyplot as plt
import numpy as np

# Example data
x1, y1 = 1, 2  # First point
x2, y2 = 4, 6  # Second point

# Create a plot
plt.plot([0, 5], [0, 7], label="Line")  # Just for context, a line plot
plt.scatter([x1, x2], [y1, y2], color='red')  # Scatter the points

# Draw an arrow between the points
plt.annotate('', xy=(x2, y2), xytext=(x1, y1),
             arrowprops=dict(facecolor='blue', edgecolor='blue', arrowstyle='->', lw=2))

# Add labels and title
plt.xlabel('x')
plt.ylabel('y')
plt.title('Arrow Between Points')

# Show the plot
plt.show()
