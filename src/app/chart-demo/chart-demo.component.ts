import { Component } from '@angular/core';
import { LineChartComponent } from '../components/line-chart/line-chart.component';
import { VerticalBarChartComponent } from '../components/vertical-bar-chart/vertical-bar-chart.component';
import { HorizontalBarChartComponent } from '../components/horizontal-bar-chart/horizontal-bar-chart.component';
import { PieChartComponent } from '../components/pie-chart/pie-chart.component';

@Component({
  selector: 'app-chart-demo',
  imports:[LineChartComponent,VerticalBarChartComponent,HorizontalBarChartComponent,PieChartComponent],
  templateUrl: './chart-demo.component.html',
  styleUrls: ['./chart-demo.component.scss'],
})
export class ChartDemoComponent {
  // Line Chart Data
  lineData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    datasets: [
      { data: [10, 20, 30, 40, 50], label: 'Stock Prices' }
    ]
  };
  PieData = {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
    datasets: [
      { data: [10, 20, 30, 40, 50], label: 'Expenses' }
    ]
  };

  // Vertical Bar Chart Data
  verticalBarData = {
    labels: ['Product A', 'Product B', 'Product C', 'Product D'],
    datasets: [
      { data: [100, 200, 300, 400], label: 'Sales' }
    ]
  };

  // Horizontal Bar Chart Data
  horizontalBarData = {
    labels: ['Apple', 'Banana', 'Mango', 'Grapes'],
    datasets: [
      { data: [50, 75, 100, 125], label: 'Fruit Sales' }
    ]
  };

  // Common Chart Options
  chartOptions = {
    responsive: true,
    plugins: { legend: { display: true } }
  };
}
