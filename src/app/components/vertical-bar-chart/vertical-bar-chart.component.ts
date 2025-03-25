import { Component, Input, OnChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChartConfiguration, ChartType } from 'chart.js';
import { BaseChartDirective } from 'ng2-charts';

@Component({
  selector: 'app-vertical-bar-chart',
  standalone:true,
  imports: [CommonModule, BaseChartDirective],
  templateUrl: './vertical-bar-chart.component.html',
})
export class VerticalBarChartComponent implements OnChanges {
  @Input() barChartData!: ChartConfiguration['data'];
  @Input() barChartOptions: ChartConfiguration['options'] = { 
    responsive: true,
    indexAxis: 'x'  
  };

  barChartType: ChartType = 'bar';

  ngOnChanges() {
    if (this.barChartData?.datasets) {
      this.barChartData.datasets.forEach((dataset) => {
        dataset.backgroundColor = this.generateColors(dataset.data.length);
      });
      console.log('Chart Type:', this.barChartType);
      console.log('Chart Options:', this.barChartOptions);
    }
    if (this.barChartOptions) {
      this.barChartOptions.indexAxis = 'x';
    }
  }

  generateColors(count: number): string[] {
    return Array.from({ length: count }, () => 
      `#${Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0')}`
    );
  }
}
