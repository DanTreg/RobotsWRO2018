namespace ASP.NET_MVC_Application.Models
{
    public class ProductMoveModel
    {
        public int RobotNumber { get; set; }
        public string ProductName { get; set; }
        public Place Place { get; set; }
        public bool Freshness { get; set; }
        public bool Temperature { get; set; }
    }
}