import { Component, Input, OnChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChartConfiguration, ChartType } from 'chart.js';
import { BaseChartDirective } from 'ng2-charts';

@Component({
  selector: 'app-line-chart',
  standalone:true,
  imports: [CommonModule, BaseChartDirective],
  templateUrl: './line-chart.component.html',
})
export class LineChartComponent implements OnChanges {
  @Input() lineChartData!: ChartConfiguration['data'];
  @Input() lineChartOptions: ChartConfiguration['options'] = { responsive: true };

  lineChartType: ChartType = 'line';

  ngOnChanges() {
    if (this.lineChartData?.datasets) {
      this.lineChartData.datasets.forEach((dataset, index) => {
        dataset.borderColor = this.generateColors(1)[0];
        dataset.backgroundColor = this.generateColors(1)[0] + '33'; // Transparent fill
      });
    }
  }

  generateColors(count: number): string[] {
    return Array.from({ length: count }, () => 
      `#${Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0')}`
    );
  }
}
