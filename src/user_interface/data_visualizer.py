# import pandas
# import seaborn
# import matplotlib


# class DataVisualizer:
#   def __init__(self):
#     self.sample_data = pandas.DataFrame({'Category': ['A', 'B', 'C', 'D', 'E'], 'Value': [10, 20, 15, 25, 30]})

#   def plot_bar_chart(self):
#     matplotlib.pyplot.figure(figsize=(8, 6))
#     seaborn.barplot(x='Category', y='Value', data=self.sample_data)
#     matplotlib.pyplot.title('Sample Bar Chart')
#     matplotlib.pyplot.xlabel('Category')
#     matplotlib.pyplot.ylabel('Value')
#     matplotlib.pyplot.tight_layout()
#     return matplotlib.pyplot

#   def plot_pie_chart(self):
#     matplotlib.pyplot.figure(figsize=(8, 6))
#     matplotlib.pyplot.pie(self.sample_data['Value'], labels=self.sample_data['Category'], autopct='%1.1f%%')
#     matplotlib.pyplot.title('Sample Pie Chart')
#     matplotlib.pyplot.tight_layout()
#     return matplotlib.pyplot