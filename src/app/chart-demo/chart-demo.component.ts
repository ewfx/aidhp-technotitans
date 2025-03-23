import { Component } from '@angular/core';
import { ChartConfiguration } from 'chart.js';
import { LineChartComponent } from '../components/line-chart/line-chart.component';
import { VerticalBarChartComponent } from '../components/vertical-bar-chart/vertical-bar-chart.component';
import { HorizontalBarChartComponent } from '../components/horizontal-bar-chart/horizontal-bar-chart.component';
import { PieChartComponent } from '../components/pie-chart/pie-chart.component';

@Component({
  selector: 'app-chart-demo',
  standalone: true,
  imports: [
    LineChartComponent,
    VerticalBarChartComponent,
    HorizontalBarChartComponent,
    PieChartComponent
  ],
  templateUrl: './chart-demo.component.html',
  styleUrls: ['./chart-demo.component.scss'],
})
export class ChartDemoComponent {
  /** 📊 Line Chart Data */
  lineData: ChartConfiguration['data'] = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    datasets: [
      { data: [10, 20, 30, 40, 50] }
    ]
  };

  /** 🥧 Pie Chart Data */
  pieData: ChartConfiguration['data'] = {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
    datasets: [
      { data: [10, 20, 30, 40, 50] } 
    ]
  };

  /** 📊 Vertical Bar Chart Data */
  verticalBarData: ChartConfiguration['data'] = {
    labels: ['Product A', 'Product B', 'Product C', 'Product D'],
    datasets: [
      { data: [100, 200, 300, 400] }
    ]
  };

  /** 📊 Horizontal Bar Chart Data */
  horizontalBarData: ChartConfiguration['data'] = {
    labels: ['Apple', 'Banana', 'Mango', 'Grapes'],
    datasets: [
      { data: [50, 75, 100, 125]}
    ]
  };
  verticalBarChartOptions: ChartConfiguration['options'] = {
    responsive: true,
    indexAxis: 'x',
    plugins: { 
      legend: { display: true },
      title: { display: true, text: 'Product Sales (Vertical Bar Chart)' }
    }
  };
  
  horizontalBarChartOptions: ChartConfiguration['options'] = {
    responsive: true,
    indexAxis: 'y',
    plugins: { 
      legend: {  position: 'top'  },
      title: { display: true, text: 'Fruit Sales ' }
    }
  };
  
  pieChartOptions: ChartConfiguration['options'] = {
    responsive: true,
    plugins: { 
      legend: {  position: 'top' },
     
    }
  };
  
  lineChartOptions: ChartConfiguration['options'] = {
    responsive: true,
    plugins: { 
      legend: { display: true },
      title: { display: true, text: 'Stock Price Trends ' }
    },
    elements: { line: { tension: 0.4 } }
  };
}  