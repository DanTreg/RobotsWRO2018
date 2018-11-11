using System;
using System.Collections.Generic;
using System.Linq;
using ASP.NET_MVC_Application.Extensions;
using ASP.NET_MVC_Application.Models;

namespace ASP.NET_MVC_Application.Repositories
{
    public class ProductRepository : BaseRepository<Product>
    {
        protected override string EntityName => "Products";

        //get product list

        public override List<Product> GetAll(bool includeDeleted = false)
        {
            var list = base.GetAll(includeDeleted);
            list.ForEach(x => x.ExpirationStatus = SetExpirationStatus(x.ExpirationDate, x.ExpirationStatus));
            return list;
        }

        //find product by name

        public Product GetByName(string name)
        {
            var all = GetAll();
            var ent = all.Find(x => x.Name == name);
            return ent;
        }


        public int SetExpirationStatus(DateTime ExpirationDate, int currentStatus)
        {
            int result = 1;
            int expirationstatus = 1;
            if (DateTime.Now.Date.AddDays(7) < ExpirationDate.Date && currentStatus != 4)
            {
                expirationstatus = 2;
            }

            if ((DateTime.Now.Date < ExpirationDate.Date) && (ExpirationDate.Date < DateTime.Now.Date.AddDays(7)) && (currentStatus != 4))
            {
                expirationstatus = 3;
            }

            if (DateTime.Now >= ExpirationDate.Date)
            {
                expirationstatus = 4;
            }

            if (currentStatus == 4)
            {
                expirationstatus = 4;
            }

            result = expirationstatus;

            return result;
        }

    }

    //Создание новой записи блокчейн, записи различаются есть или нет айди продукта, в случае Alert айди продукта = null и не участвует в записи
    //Create new blockchain record
    public class ProductBlockchainRepository : BaseRepository<ProductBlockchain>
    {
        protected override string EntityName => "ProductBlockchain";

        public override ProductBlockchain Create(ProductBlockchain blockchain)
        {
            var rand = new Random(); //random integer
            var currentTime = DateTime.Now; //current date time
            var word = "";
            var last = GetAll().OrderByDescending(x => x.Id).FirstOrDefault(); //get last record hash if exists
            if (blockchain.ProductId is null)
            {
                word = $"{last?.Hash}:{blockchain.Comment}:{currentTime.ToString()}:{rand.ToString()}"; //create new blockchain record
            }
            else
            {
                word = $"{last?.Hash}:{blockchain.Comment}:{blockchain.ProductId}:{currentTime.ToString()}:{rand.ToString()}"; //forming new blockchain record
            }
            blockchain.Hash = CryptographyExtensions.GetHashSha256(word);

            return base.Create(blockchain);

        }

    }

    public class RobotRepository : BaseRepository<Robot>
    {
        protected override string EntityName => "Robot";

        //get product list

        public override List<Robot> GetAll(bool includeDeleted = false)
        {
            var list = base.GetAll(includeDeleted);

            return list;
        }

        //find product by name

        public Robot GetByName(string name)
        {
            var all = GetAll();
            var ent = all.Find(x => x.Name == name);
            return ent;
        }
    }


    public class MachinesRepository : BaseRepository<Machines>
    {
        protected override string EntityName => "Machines";
    }

}