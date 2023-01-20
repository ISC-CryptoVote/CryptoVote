import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-box-button',
  templateUrl: './box-button.component.html',
  styleUrls: ['./box-button.component.css']
})
export class BoxButtonComponent {
  @Output() onaction: EventEmitter<any> = new EventEmitter();
  @Input() title: string = "";
  @Input() icon: string = "";

  run(){
    console.log("OK")
    this.onaction.emit()
  }
}
